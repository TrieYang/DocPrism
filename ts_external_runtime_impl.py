"""
Resolve runtime implementation artifacts for external dependency *declaration* surfaces.

When navigation lands on `node_modules/**.d.ts` (or similar), try—in order:
  1) LSP `textDocument/implementation` from the declaration position (after didOpen).
  2) TypeScript declaration map (`*.d.ts.map`) → linked source file, then locate symbol.
  3) Sibling runtime modules (`name.js` / `.mjs` / `.cjs` next to `name.d.ts`), then locate symbol.
  4) When the runtime hit is a cross-module export alias (`exports.foo = mod.foo`, TS emit
     `(0, mod_1.foo)`, etc.), follow `require` / `import` bindings to the defining module.

This does not guarantee original author TypeScript; it prefers concrete `.ts`/`.js` over `.d.ts`
when the package publishes them and the link exists.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from lsp_client import GenericLSPClient, Location, file_uri, uri_to_path

_DECLARATION_SURFACE_SUFFIXES = (".d.ts", ".d.cts", ".d.mts")

try:
    from tree_sitter_language_pack import get_parser
except ImportError:
    try:
        from tree_sitter_languages import get_parser
    except ImportError:
        try:
            from code_navigation_TypeScript import get_parser  # tree-sitter-* grammars
        except ImportError:
            get_parser = None  # type: ignore[assignment]


def is_declaration_surface(path: Path) -> bool:
    """True for TypeScript declaration files (.d.ts, .d.cts, .d.mts, …)."""
    name = path.name.lower()
    return any(name.endswith(suffix) for suffix in _DECLARATION_SURFACE_SUFFIXES)


def declaration_stem(path: Path) -> Optional[str]:
    """Module stem for `foo.d.ts` / `foo.d.cts` → `foo`."""
    for suffix in _DECLARATION_SURFACE_SUFFIXES:
        if path.name.endswith(suffix):
            return path.name[: -len(suffix)]
    return None


@dataclass(frozen=True)
class ExternalRuntimeResolution:
    """Runtime export surface plus optional deeper implementation (re-export target)."""

    loc: Location
    method: str
    trace: Dict[str, Any]
    implementation_loc: Optional[Location] = None


def should_attempt_external_runtime_resolution(
    def_path: Path,
    *,
    repo_root: Path,
) -> bool:
    """True when the current target is an external declaration surface worth upgrading."""
    try:
        def_path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return False
    s = str(def_path).replace("\\", "/")
    if "node_modules/" not in s:
        return False
    return is_declaration_surface(def_path)


def _rank_runtime_locations(locs: List[Location]) -> List[Location]:
    """Prefer non-.d.ts, then .ts over .js; deprioritize minified bundles."""

    def sort_key(L: Location) -> Tuple[int, int, str]:
        p = uri_to_path(L.uri)
        name = p.name.lower()
        if is_declaration_surface(p):
            tier = 0
        elif p.suffix in (".ts", ".tsx"):
            tier = 4
        elif ".min." in name or name.endswith(".min.js"):
            tier = 1
        elif p.suffix in (".js", ".mjs", ".cjs"):
            tier = 3
        elif p.suffix in (".mts", ".cts"):
            tier = 4
        else:
            tier = 2
        return (-tier, len(str(p)), str(p))

    return sorted(locs, key=sort_key)


_MODULE_EXTENSIONS = ("", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts")
_INDEX_EXTENSIONS = (".js", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts")
_ALIAS_FOLLOW_MAX_DEPTH = 4


def _resolve_relative_module(base_dir: Path, spec: str) -> Optional[Path]:
    """Resolve a relative import/require specifier to an existing file."""
    spec = spec.strip()
    if not spec.startswith("."):
        return None
    base = (base_dir / spec).resolve()
    if base.is_file():
        return base
    for ext in _MODULE_EXTENSIONS:
        if not ext:
            continue
        candidate = Path(str(base) + ext)
        if candidate.is_file():
            return candidate.resolve()
    if base.is_dir():
        for ext in _INDEX_EXTENSIONS:
            candidate = base / f"index{ext}"
            if candidate.is_file():
                return candidate.resolve()
    for ext in _INDEX_EXTENSIONS:
        candidate = base.parent / f"{base.name}{ext}" if base.suffix else Path(str(base) + ext)
        if candidate.is_file():
            return candidate.resolve()
    index_base = base if base.suffix else base
    for ext in _INDEX_EXTENSIONS:
        candidate = index_base / f"index{ext}"
        if candidate.is_file():
            return candidate.resolve()
    return None


def _collect_module_bindings(path: Path) -> Dict[str, Path]:
    """
    Map local binding names to resolved module paths from require/import forms, e.g.:
      var _ = __importStar(require("./internal"));
      import * as M from "./mod";
    """
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    base_dir = path.parent
    bindings: Dict[str, Path] = {}

    def add(name: str, spec: str) -> None:
        name = name.strip()
        if not name or name in bindings:
            return
        resolved = _resolve_relative_module(base_dir, spec)
        if resolved is not None:
            bindings[name] = resolved

    for m in re.finditer(
        r"(?:var|let|const)\s+(\w+)\s*=\s*require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
        source,
    ):
        add(m.group(1), m.group(2))
    for m in re.finditer(
        r"(?:var|let|const)\s+(\w+)\s*=\s*__import(?:Star|Default)?\s*\(\s*require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\)",
        source,
    ):
        add(m.group(1), m.group(2))
    for m in re.finditer(
        r"import\s+\*\s+as\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]",
        source,
    ):
        add(m.group(1), m.group(2))
    for m in re.finditer(
        r"import\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]",
        source,
    ):
        add(m.group(1), m.group(2))
    for m in re.finditer(
        r"import\s+\{([^}]+)\}\s+from\s+['\"]([^'\"]+)['\"]",
        source,
    ):
        spec = m.group(2)
        resolved = _resolve_relative_module(base_dir, spec)
        if resolved is None:
            continue
        for part in m.group(1).split(","):
            part = part.strip()
            if not part:
                continue
            alias = part
            if " as " in part:
                _, alias = part.split(" as ", 1)
            alias = alias.strip()
            if alias:
                bindings[alias] = resolved
    return bindings


def _rhs_is_inline_implementation(rhs_text: str) -> bool:
    """True when RHS text is a direct implementation, not a cross-module alias."""
    t = rhs_text.strip().rstrip(";").strip()
    if not t:
        return False
    if t.startswith("function") or t.startswith("async function"):
        return True
    if "=>" in t and ("(" in t or re.match(r"^\w+\s*=>", t)):
        return True
    if t.startswith("{") or t.startswith("["):
        return True
    if t.startswith("class "):
        return True
    return False


def _parse_export_alias_rhs(rhs_text: str, symbol: str) -> Optional[Tuple[str, str]]:
    """
    Parse export-assignment RHS into (binding_ident, member_name).
    Returns None when RHS is an inline implementation or unrecognized.
    """
    t = rhs_text.strip().rstrip(";").strip()
    if not t or _rhs_is_inline_implementation(t):
        return None

    # TypeScript emit: (0, module_1.symbol)
    m = re.match(r"^\(\s*0\s*,\s*(\w+)\.(\w+)\s*\)$", t)
    if m:
        return m.group(1), m.group(2)

    # binding.member (possibly same member as exported symbol)
    m = re.match(r"^(\w+)\.(\w+)$", t)
    if m:
        return m.group(1), m.group(2)

    # exports.foo = foo — re-export local or imported binding under same name
    m = re.match(r"^(\w+)$", t)
    if m:
        return m.group(1), symbol

    return None


def _parse_export_alias_from_line(line: str, symbol: str) -> Optional[Tuple[str, str]]:
    """Detect `exports.sym = …` / `module.exports.sym = …` alias assignments."""
    esc = re.escape(symbol)
    m = re.match(
        rf"^\s*(?:module\.)?exports\.{esc}\s*=\s*(.+?)\s*;?\s*$",
        line.strip(),
    )
    if not m:
        return None
    return _parse_export_alias_rhs(m.group(1), symbol)


def _line_is_export_alias(line: str, symbol: str) -> bool:
    return _parse_export_alias_from_line(line, symbol) is not None


def _follow_module_export_alias(
    path: Path,
    loc: Location,
    symbol: str,
    *,
    depth: int = 0,
    visited: Optional[set[Tuple[str, str]]] = None,
) -> Optional[Location]:
    """
    When ``loc`` points at ``exports.<symbol> = alias.member`` (or similar),
    resolve the module behind ``alias`` and locate the real implementation.
    """
    if depth >= _ALIAS_FOLLOW_MAX_DEPTH or not symbol:
        return None
    if visited is None:
        visited = set()
    key = (str(path.resolve()), symbol)
    if key in visited:
        return None
    visited.add(key)

    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    if loc.start_line < 0 or loc.start_line >= len(lines):
        return None

    alias = _parse_export_alias_from_line(lines[loc.start_line], symbol)
    if alias is None:
        return None

    binding, member = alias
    module_bindings = _collect_module_bindings(path)

    if binding in module_bindings:
        target_path = module_bindings[binding]
        target_loc = _location_for_implementation_in_file(
            target_path, member, _follow_aliases=False
        )
        if uri_to_path(target_loc.uri) != target_path:
            target_loc = _location_for_symbol_in_file(target_path, member)
        deeper = _follow_module_export_alias(
            target_path,
            target_loc,
            member,
            depth=depth + 1,
            visited=visited,
        )
        return deeper or target_loc

    # Same-file binding: `exports.foo = foo` where foo is defined locally.
    local_impl = _ast_implementation_for_symbol(path, member)
    if local_impl is not None:
        impl_path = uri_to_path(local_impl.uri)
        if impl_path.resolve() == path.resolve():
            return local_impl

    return None


def _ast_implementation_for_symbol(path: Path, symbol: str) -> Optional[Location]:
    parser = _ts_parser_for_path(path)
    if parser is None or not symbol:
        return None
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    
    source_bytes = source.encode("utf-8")
    
    try:
        tree = parser.parse(source_bytes)
    except Exception:
        return None
    root = tree.root_node
    if root is None or root.has_error:
        return None
    uri = file_uri(path.resolve())

    def _loc_from_node(node) -> Location:
        sl, sc = node.start_point
        el, ec = node.end_point
        return Location(uri, int(sl), int(sc), int(el), int(ec))

    def _declarator_is_implementation(declarator) -> bool:
        value = declarator.child_by_field_name("value")
        if value is None:
            return False
        if value.type in ("function", "arrow_function", "class", "object", "array"):
            return True
        value_text = _node_text(source_bytes, value).strip()
        return _rhs_is_inline_implementation(value_text)

    def walk(node) -> Optional[Location]:
        if node.type in ("function_declaration", "method_definition"):
            name_node = node.child_by_field_name("name")
            if name_node is not None and _node_text(source_bytes, name_node) == symbol:
                return _loc_from_node(node)

        if node.type in ("lexical_declaration", "variable_declaration"):
            for i in range(node.child_count):
                child = node.child(i)
                if child.type != "variable_declarator":
                    continue
                name_node = child.child_by_field_name("name")
                if name_node is None or _node_text(source_bytes, name_node) != symbol:
                    continue
                if _declarator_is_implementation(child):
                    return _loc_from_node(child)

        for i in range(node.child_count):
            found = walk(node.child(i))
            if found is not None:
                return found
        return None

    return walk(root)


def _ast_export_assignment_for_symbol(path: Path, symbol: str) -> Optional[Location]:
    parser = _ts_parser_for_path(path)
    if parser is None or not symbol:
        return None
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    source_bytes = source.encode("utf-8")
    try:
        tree = parser.parse(source_bytes)
    except Exception:
        return None
    root = tree.root_node
    if root is None or root.has_error:
        return None
    uri = file_uri(path.resolve())

    def _loc_from_node(node) -> Location:
        sl, sc = node.start_point
        el, ec = node.end_point
        return Location(uri, int(sl), int(sc), int(el), int(ec))

    def walk(node) -> Optional[Location]:
        if node.type == "assignment_expression":
            left = node.child_by_field_name("left")
            if left is not None and left.type == "member_expression":
                prop = left.child_by_field_name("property")
                if prop is not None and _node_text(source_bytes, prop) == symbol:
                    obj = left.child_by_field_name("object")
                    obj_text = _node_text(source_bytes, obj).strip() if obj is not None else ""
                    if obj_text in ("exports", "module.exports"):
                        return _loc_from_node(node)
        for i in range(node.child_count):
            found = walk(node.child(i))
            if found is not None:
                return found
        return None

    return walk(root)


def _locations_equivalent(a: Location, b: Location) -> bool:
    return (
        a.uri == b.uri
        and a.start_line == b.start_line
        and a.start_char == b.start_char
        and a.end_line == b.end_line
        and a.end_char == b.end_char
    )


def _regex_location_for_symbol(path: Path, symbol: Optional[str]) -> Optional[Location]:
    """Line-anchored regex scan — primary locator for runtime symbols in .js/.ts emit."""
    if not symbol:
        return None
    uri = file_uri(path.resolve())
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for i, line in enumerate(lines):
        if _line_declares_symbol(line, symbol):
            return Location(uri, i, 0, i, max(0, len(line) - 1))
    return None


def _acceptable_ast_export_assignment(path: Path, loc: Location, symbol: str) -> bool:
    """
    AST export hits can land on mid-line bulk emit (``exports.a = exports.b = void 0``).
    Only accept when the full source line also passes the line-anchored regex check.
    """
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return False
    if loc.start_line < 0 or loc.start_line >= len(lines):
        return False
    return _line_declares_symbol(lines[loc.start_line], symbol)


def _location_for_export_surface_in_file(path: Path, symbol: Optional[str]) -> Location:
    """
    Find the export line or in-file implementation — never follow cross-module aliases.

    Resolution order:
      1) Regex line scan (line-anchored; skips mid-line bulk ``exports.* = void 0`` emit)
      2) AST ``var``/``function`` implementation backup when regex finds nothing
      3) AST ``exports.*`` assignment only as last resort, and only if the line passes (1)
    """
    uri = file_uri(path.resolve())
    if not symbol:
        return Location(uri, 0, 0, min(40, max(0, _line_count(path) - 1)), 0)

    regex_loc = _regex_location_for_symbol(path, symbol)
    if regex_loc is not None:
        return regex_loc

    impl = _ast_implementation_for_symbol(path, symbol)
    if impl is not None:
        return impl

    export_loc = _ast_export_assignment_for_symbol(path, symbol)
    if export_loc is not None and _acceptable_ast_export_assignment(path, export_loc, symbol):
        return export_loc

    return Location(uri, 0, 0, min(40, max(0, _line_count(path) - 1)), 0)


def _location_for_implementation_in_file(
    path: Path,
    symbol: Optional[str],
    *,
    _follow_aliases: bool = True,
) -> Location:
    """Prefer concrete implementations; optionally follow export aliases to other modules."""
    surface = _location_for_export_surface_in_file(path, symbol)
    if not symbol or not _follow_aliases:
        return surface
    try:
        line = path.read_text(encoding="utf-8", errors="replace").splitlines()[
            surface.start_line
        ]
    except (OSError, IndexError):
        return surface
    if _line_is_export_alias(line, symbol):
        followed = _follow_module_export_alias(path, surface, symbol)
        if followed is not None:
            return followed
    return surface


def _location_for_symbol_in_file(path: Path, symbol: Optional[str]) -> Location:
    return _location_for_implementation_in_file(path, symbol, _follow_aliases=True)


def _resolve_export_surface_and_implementation(
    path: Path,
    symbol: Optional[str],
    trace: Optional[Dict[str, Any]] = None,
) -> Tuple[Location, Optional[Location]]:
    """
    Return (export_surface, optional_implementation).
    The export surface keeps public docs / re-export lines; implementation is a
    bonus when the surface is a cross-module alias.
    """
    surface = _location_for_export_surface_in_file(path, symbol)
    if not symbol:
        return surface, None
    try:
        line = path.read_text(encoding="utf-8", errors="replace").splitlines()[
            surface.start_line
        ]
    except (OSError, IndexError):
        return surface, None

    implementation: Optional[Location] = None
    if _line_is_export_alias(line, symbol):
        implementation = _follow_module_export_alias(path, surface, symbol)
        if implementation is not None and trace is not None:
            trace.setdefault("attempts", []).append(
                {
                    "step": "follow_module_export_alias",
                    "from": path.as_posix(),
                    "to": uri_to_path(implementation.uri).as_posix(),
                    "symbol": symbol,
                }
            )

    if implementation is not None and _locations_equivalent(surface, implementation):
        implementation = None

    return surface, implementation


def _finalize_runtime_location(
    path: Path,
    loc: Location,
    symbol: Optional[str],
    trace: Dict[str, Any],
) -> Tuple[Location, Optional[Location]]:
    """Split an LSP/runtime hit into export surface vs optional followed implementation."""
    if not symbol:
        return loc, None
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return loc, None
    if loc.start_line < 0 or loc.start_line >= len(lines):
        return loc, None

    line = lines[loc.start_line]
    if _line_is_export_alias(line, symbol):
        surface = loc
        implementation = _follow_module_export_alias(path, surface, symbol)
        if implementation is not None:
            trace.setdefault("attempts", []).append(
                {
                    "step": "follow_module_export_alias",
                    "from": path.as_posix(),
                    "to": uri_to_path(implementation.uri).as_posix(),
                    "symbol": symbol,
                }
            )
        return surface, implementation

    return loc, loc if not is_declaration_surface(path) else None


def _line_declares_symbol(line: str, symbol: str) -> bool:
    if not symbol:
        return False
    esc = re.escape(symbol)
    patterns = (
        rf"^\s*export\s+async\s+function\s+{esc}\b",
        rf"^\s*export\s+function\s+{esc}\b",
        rf"^\s*async\s+function\s+{esc}\b",
        rf"^\s*function\s+{esc}\b",
        rf"^\s*export\s+const\s+{esc}\b",
        rf"^\s*export\s+let\s+{esc}\b",
        rf"^\s*export\s+var\s+{esc}\b",
        rf"^\s*const\s+{esc}\b",
        rf"^\s*let\s+{esc}\b",
        rf"^\s*var\s+{esc}\b",
        rf"^\s*exports\.{esc}\s*=",
        rf"^\s*module\.exports\.{esc}\s*=",
        rf"^\s*export\s+declare\s+function\s+{esc}\b",  # rare in .ts emit
        rf"^\s*(?:public|private|protected|static|readonly|abstract|override|declare)\s+(?:async\s+)?{esc}\b\s*[\(<]",
        rf"^\s*(?:async\s+)?{esc}\s*\(",  # class/object method in emitted JS/TS
        rf"^\s*{esc}\s*[:=]\s*(async\s*)?(\([^)]*\)|<[^>]+>)\s*=>",
        rf"^\s*{esc}\s*[:=]\s*function\b",
    )
    return any(re.search(p, line) for p in patterns)


def _ts_parser_for_path(path: Path):
    if get_parser is None:
        return None
    ext = path.suffix.lower()
    try:
        if ext in (".ts", ".tsx", ".mts", ".cts"):
            return get_parser("typescript")
        if ext in (".js", ".jsx", ".mjs", ".cjs"):
            return get_parser("javascript")
    except Exception:
        return None
    return None


def _node_text(source_bytes: bytes, node) -> str:
    if node is None:
        return ""
    return source_bytes[node.start_byte: node.end_byte].decode("utf-8", errors="replace")


def _line_count(path: Path) -> int:
    try:
        return sum(1 for _ in path.open(encoding="utf-8", errors="replace"))
    except OSError:
        return 0


def _resolve_via_declaration_map(
    d_ts: Path, symbol: Optional[str]
) -> Optional[Location]:
    map_path = d_ts.parent / (d_ts.name + ".map")
    if not map_path.is_file():
        return None
    try:
        data = json.loads(map_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    sources = data.get("sources")
    if not sources or not isinstance(sources, list):
        return None
    rel = sources[0]
    if not isinstance(rel, str) or not rel:
        return None
    target = (d_ts.parent / rel).resolve()
    if not target.is_file():
        return None
    if target.suffix not in (".ts", ".tsx", ".js", ".mjs", ".cjs", ".mts", ".cts"):
        return None
    return _location_for_symbol_in_file(target, symbol)


def _parallel_module_candidates(decl_path: Path) -> List[Path]:
    stem = declaration_stem(decl_path)
    if stem is None:
        return []
    base = decl_path.parent
    out: List[Path] = []
    for ext in (".ts", ".tsx", ".mts", ".cts", ".js", ".mjs", ".cjs"):
        p = base / f"{stem}{ext}"
        if p.is_file():
            out.append(p.resolve())
    return out


def symbol_located_in_file(
    path: Path, loc: Location, symbol: Optional[str]
) -> bool:
    """True when ``symbol`` has a concrete hit in ``path`` (not a line-0 fallback window)."""
    if not symbol:
        return True
    if _regex_location_for_symbol(path, symbol) is not None:
        return True
    if _ast_implementation_for_symbol(path, symbol) is not None:
        return True
    export_loc = _ast_export_assignment_for_symbol(path, symbol)
    if export_loc is not None and _acceptable_ast_export_assignment(path, export_loc, symbol):
        return True
    return False


def try_resolve_external_runtime_implementation(
    *,
    client: GenericLSPClient,
    declaration_loc: Location,
    declaration_path: Path,
    symbol_name: Optional[str],
) -> Optional[ExternalRuntimeResolution]:
    """
    From a position inside an external .d.ts, attempt to find a runtime/source file
    and a best-effort position for the same symbol.
    """
    trace: Dict[str, Any] = {"attempts": []}

    if not is_declaration_surface(declaration_path):
        return None

    # 1) LSP implementation from declaration site
    try:
        decl_uri = declaration_loc.uri
        decl_text = declaration_path.read_text(encoding="utf-8", errors="replace")
        client.open_document(decl_uri, decl_text)
        impl_locs = client.goto_implementation(
            decl_uri,
            declaration_loc.start_line,
            declaration_loc.start_char,
        )
        trace["attempts"].append({"step": "lsp_implementation", "count": len(impl_locs)})
        ranked = _rank_runtime_locations(impl_locs)
        for loc in ranked:
            p = uri_to_path(loc.uri)
            if is_declaration_surface(p):
                continue
            if not p.is_file():
                continue
            surface, implementation = _finalize_runtime_location(
                p, loc, symbol_name, trace
            )
            return ExternalRuntimeResolution(
                loc=surface,
                method="lsp_implementation",
                trace={**trace, "chosen_path": str(p)},
                implementation_loc=implementation,
            )
        # Some TS servers return another declaration first; try one more hop.
        second_hop: List[Location] = []
        for loc in ranked:
            p = uri_to_path(loc.uri)
            if is_declaration_surface(p):
                continue
            try:
                second = client.goto_implementation(
                    loc.uri, loc.start_line, loc.start_char
                )
                second_hop.extend(second)
            except Exception:
                continue
        if second_hop:
            ranked_second = _rank_runtime_locations(second_hop)
            trace["attempts"].append(
                {"step": "lsp_implementation_second_hop", "count": len(second_hop)}
            )
            for loc in ranked_second:
                p = uri_to_path(loc.uri)
                if is_declaration_surface(p):
                    continue
                if not p.is_file():
                    continue
                surface, implementation = _finalize_runtime_location(
                    p, loc, symbol_name, trace
                )
                return ExternalRuntimeResolution(
                    loc=surface,
                    method="lsp_implementation_second_hop",
                    trace={**trace, "chosen_path": str(p)},
                    implementation_loc=implementation,
                )
    except Exception as e:
        trace["attempts"].append({"step": "lsp_implementation", "error": str(e)})

    # 2) Declaration map
    try:
        mapped = _resolve_via_declaration_map(declaration_path, symbol_name)
        if mapped is not None:
            mp = uri_to_path(mapped.uri)
            surface, implementation = _finalize_runtime_location(
                mp, mapped, symbol_name, trace
            )
            trace["attempts"].append(
                {"step": "declaration_map", "path": uri_to_path(surface.uri).as_posix()}
            )
            return ExternalRuntimeResolution(
                loc=surface,
                method="declaration_map",
                trace={**trace},
                implementation_loc=implementation,
            )
    except Exception as e:
        trace["attempts"].append({"step": "declaration_map", "error": str(e)})

    # 3) Sibling .ts / .js next to .d.ts
    try:
        for cand in _parallel_module_candidates(declaration_path):
            if is_declaration_surface(cand):
                continue
            surface, implementation = _resolve_export_surface_and_implementation(
                cand, symbol_name, trace
            )
            if symbol_name and implementation is None:
                if not symbol_located_in_file(cand, surface, symbol_name):
                    trace["attempts"].append(
                        {
                            "step": "sibling_module",
                            "path": cand.as_posix(),
                            "skipped": "symbol_not_in_runtime_file",
                        }
                    )
                    continue
            trace["attempts"].append(
                {"step": "sibling_module", "path": cand.as_posix()}
            )
            return ExternalRuntimeResolution(
                loc=surface,
                method="sibling_module",
                trace={
                    **trace,
                    "chosen_path": cand.as_posix(),
                    "export_surface_path": uri_to_path(surface.uri).as_posix(),
                },
                implementation_loc=implementation,
            )
    except Exception as e:
        trace["attempts"].append({"step": "sibling_module", "error": str(e)})

    return None


def snippet_fallback_from_location(loc: Location, max_lines: int = 120) -> str:
    """Read a bounded window around an LSP range (works for JS/TS)."""
    p = uri_to_path(loc.uri)
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    start = max(0, loc.start_line)
    end = min(len(lines), max(loc.end_line + 1, start + 1, start + max_lines))
    return "\n".join(lines[start:end])
