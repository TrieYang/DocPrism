"""Shared TypeScript definition-selection helpers for phase 3/4 resolution."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from lsp_client import GenericLSPClient, Location, uri_to_path
from models import DefCandidate
from ts_ast import (
    TREE_SITTER_AVAILABLE as _TREE_SITTER_AVAILABLE,
    ancestors_include_type as _ancestors_include_type,
    find_node_at_point as _find_node_at_point,
    get_ts_parser as _get_ts_parser,
)


def _get_referenced_type_on_line(line: str) -> Optional[Tuple[str, int]]:
    """
    If line looks like a declaration with a type (e.g. '  name: TypeName;'),
    return (TypeName, character_offset_of_TypeName). Otherwise None.
    """
    m = re.search(r":\s*([A-Za-z_$][A-Za-z0-9_$]*)", line)
    if not m:
        return None
    return (m.group(1), m.start(1))


def _find_constructor_snippet(lines: List[str], symbol_name: str) -> Optional[str]:
    """
    When LSP points into an instance interface (e.g. Date, Array, Map) at a method,
    the user usually wanted the callable/constructor. TypeScript lib uses the pattern
    interface Foo { ... } and interface FooConstructor { new (...): Foo; ... }; declare var Foo.
    Find FooConstructor and return the constructor overloads plus 'declare var Foo'.
    Works for any symbol (Date, Array, Map, Set, Promise, Object, RegExp, Error, etc.).
    """
    if not symbol_name:
        return None
    esc = re.escape(symbol_name)
    constructor_interface_re = re.compile(
        r"\binterface\s+" + esc + r"Constructor\s*\{"
    )
    declare_var_re = re.compile(r"declare\s+var\s+" + esc + r"\s*:")
    new_returns_re = re.compile(r"\)\s*:\s*" + esc + r"\s*;")

    in_constructor = False
    brace_depth = 0
    snippet: List[str] = []
    for i, line in enumerate(lines):
        if constructor_interface_re.search(line):
            in_constructor = True
            brace_depth = 0
            snippet = []
        if in_constructor:
            for ch in line:
                if ch == "{":
                    brace_depth += 1
                elif ch == "}":
                    brace_depth -= 1
            snippet.append(line)
            if brace_depth == 0:
                for j in range(i + 1, min(i + 5, len(lines))):
                    if lines[j].strip() and declare_var_re.search(lines[j]):
                        snippet.append(lines[j])
                        break
                break
    if not snippet:
        return None
    out: List[str] = []
    for line in snippet:
        s = line.strip()
        if re.search(r"new\s*\(", s) and new_returns_re.search(s):
            out.append(line)
        elif declare_var_re.search(line):
            out.append(line)
    return "\n".join(out) if out else "\n".join(snippet)


def _prefer_lib_global_constructor_snippet(
    snippet: Optional[str],
    def_path: Path,
    symbol_name: Optional[str],
    *,
    usage_kind: str,
) -> Optional[str]:
    """
    lib*.d.ts models globals as interface Foo { ... } plus interface FooConstructor.
    When navigation returns the whole instance interface for a call like Date(),
    prefer FooConstructor + declare var Foo (same as _read_definition_source).
    """
    if usage_kind != "call" or not snippet or not symbol_name:
        return snippet
    if "new (" in snippet:
        return snippet
    if not re.search(r"\)\s*:\s*\w+\s*;", snippet):
        return snippet
    try:
        lines = def_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return snippet
    constructor_snippet = _find_constructor_snippet(lines, symbol_name)
    return constructor_snippet if constructor_snippet else snippet


def _definition_location_is_call_site_ast(path: Path, loc: Location) -> bool:
    """
    True if at (loc.start_line, loc.start_col) the code is inside a call_expression or
    new_expression (i.e. a call site), not a function/method declaration. Uses AST so we
    don't misclassify method definitions or other declaration forms as call sites.
    Returns False if tree-sitter is unavailable or parse fails.
    """
    if not _TREE_SITTER_AVAILABLE or not path.exists():
        return False
    parser = _get_ts_parser(path)
    if parser is None:
        return False
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        source_bytes = text.encode("utf-8")
        tree = parser.parse(source_bytes)
    except Exception:
        return False
    if tree.root_node is None or tree.root_node.has_error:
        return False

    row, col = loc.start_line, loc.start_col
    node_at = _find_node_at_point(tree.root_node, row, col)
    if node_at is None:
        return False
    return _ancestors_include_type(
        tree.root_node, node_at, ("call_expression", "new_expression")
    )


def _extract_function_range_from_symbols(
    symbols: Any,
    tested_function: str,
) -> Optional[Tuple[int, int, int, int]]:

    def from_document_symbol(sym: Dict[str, Any]) -> Optional[Tuple[int, int, int, int]]:
        if sym.get("name") != tested_function:
            return None
        rng = sym.get("range") or sym.get("selectionRange")
        if not rng:
            return None
        s = rng.get("start") or {}
        e = rng.get("end") or {}
        return (
            int(s.get("line", 0)),
            int(s.get("character", 0)),
            int(e.get("line", 0)),
            int(e.get("character", 0)),
        )

    def from_symbol_information(sym: Dict[str, Any]) -> Optional[Tuple[int, int, int, int]]:
        if sym.get("name") != tested_function:
            return None
        loc = sym.get("location") or {}
        rng = loc.get("range") or {}
        s = rng.get("start") or {}
        e = rng.get("end") or {}
        return (
            int(s.get("line", 0)),
            int(s.get("character", 0)),
            int(e.get("line", 0)),
            int(e.get("character", 0)),
        )

    if not symbols:
        return None

    if isinstance(symbols, list) and symbols and "range" in symbols[0]:
        stack = list(symbols)
        while stack:
            sym = stack.pop()
            rng = from_document_symbol(sym)
            if rng is not None:
                return rng
            children = sym.get("children") or []
            stack.extend(children)
        return None

    if isinstance(symbols, list):
        for sym in symbols:
            rng = from_symbol_information(sym)
            if rng is not None:
                return rng

    return None


def _find_symbol_location_from_document_symbols(
    symbols: Any,
    *,
    uri: str,
    symbol_name: str,
    hint_line0: int,
    parent_name_hint: Optional[str] = None,
) -> Optional[Location]:
    """
    Pick the best location for `symbol_name` from LSP document symbols.
    Prefers entries under parent_name_hint (when provided), then nearest line.
    """
    if not symbols or not symbol_name:
        return None
    parent_hint = (parent_name_hint or "").strip()
    flat: List[Tuple[int, int, int, int, List[str]]] = []

    def _rng_to_tuple(rng: Dict[str, Any]) -> Tuple[int, int, int, int]:
        s = rng.get("start") or {}
        e = rng.get("end") or {}
        return (
            int(s.get("line", 0)),
            int(s.get("character", 0)),
            int(e.get("line", 0)),
            int(e.get("character", 0)),
        )

    if isinstance(symbols, list) and symbols and "range" in symbols[0]:
        stack: List[Tuple[Dict[str, Any], List[str]]] = [(s, []) for s in symbols]
        while stack:
            sym, parents = stack.pop()
            nm = sym.get("name")
            if nm == symbol_name:
                rng = sym.get("selectionRange") or sym.get("range")
                if isinstance(rng, dict):
                    sl, sc, el, ec = _rng_to_tuple(rng)
                    flat.append((sl, sc, el, ec, list(parents)))
            for ch in sym.get("children") or []:
                stack.append((ch, parents + [str(nm or "")]))
    elif isinstance(symbols, list):
        for sym in symbols:
            if sym.get("name") != symbol_name:
                continue
            loc = sym.get("location") or {}
            rng = loc.get("range")
            if isinstance(rng, dict):
                sl, sc, el, ec = _rng_to_tuple(rng)
                flat.append((sl, sc, el, ec, []))

    if not flat:
        return None

    def _score(item: Tuple[int, int, int, int, List[str]]) -> Tuple[int, int]:
        sl, _sc, _el, _ec, parents = item
        parent_match = 0
        if parent_hint:
            parent_match = 1 if any(p == parent_hint for p in parents) else 0
        return (-parent_match, abs(sl - hint_line0))

    sl, sc, el, ec, _parents = min(flat, key=_score)
    return Location(uri, sl, sc, el, ec)


def _dedupe_locations(locs: List[Location]) -> List[Location]:
    seen = set()
    out: List[Location] = []
    for loc in locs:
        key = (loc.uri, loc.start_line, loc.start_col, loc.end_line, loc.end_col)
        if key in seen:
            continue
        seen.add(key)
        out.append(loc)
    return out


def _build_def_candidate(repo_root: Path, loc: Location) -> DefCandidate:
    from ts_external_runtime_impl import is_declaration_surface

    p = uri_to_path(loc.uri)
    is_d_ts = is_declaration_surface(p)
    try:
        _ = p.resolve().relative_to(repo_root.resolve())
        is_repo_local = True
    except Exception:
        is_repo_local = False
    in_node_modules = "node_modules" in str(p)
    return DefCandidate(
        loc=loc,
        path=p,
        is_d_ts=is_d_ts,
        in_node_modules=in_node_modules,
        is_repo_local=is_repo_local,
        path_len=len(str(p)),
    )


def _build_runtime_implementation_bundle(
    repo_root: Path,
    loc: Location,
    symbol_name: Optional[str],
    *,
    export_surface_loc: Optional[Location] = None,
) -> Dict[str, Any]:
    """
    Structured runtime payload for ``outer_definition.runtime_implementation``.

    When ``export_surface_loc`` is provided (e.g. documented ``exports.foo = mod.foo``
    before a deeper body), it is attached separately and prepended to ``full_def_source``.
    """
    from code_navigation_TypeScript import _read_definition_source

    cand = _build_def_candidate(repo_root, loc)
    src = _read_definition_source(loc, symbol_name)
    if not src or len(src.strip()) < 4:
        try:
            from ts_external_runtime_impl import snippet_fallback_from_location

            src = snippet_fallback_from_location(loc)
        except ImportError:
            pass
    bundle: Dict[str, Any] = {
        "uri": loc.uri,
        "path": cand.path.as_posix(),
        "directory": cand.path.parent.as_posix(),
        "range": {
            "start": {"line0": loc.start_line, "col0": loc.start_col},
            "end": {"line0": loc.end_line, "col0": loc.end_col},
        },
        "full_def_source": src,
    }
    try:
        rel = cand.path.resolve().relative_to(repo_root.resolve())
        bundle["repo_relative_path"] = rel.as_posix()
        bundle["repo_relative_dir"] = rel.parent.as_posix()
    except Exception:
        pass

    if export_surface_loc is not None:
        export_path = uri_to_path(export_surface_loc.uri)
        if export_path.resolve() != cand.path.resolve():
            export_cand = _build_def_candidate(repo_root, export_surface_loc)
            export_src = _read_definition_source(export_surface_loc, symbol_name)
            if not export_src or len(export_src.strip()) < 4:
                try:
                    from ts_external_runtime_impl import snippet_fallback_from_location

                    export_src = snippet_fallback_from_location(export_surface_loc)
                except ImportError:
                    export_src = ""
            export_bundle: Dict[str, Any] = {
                "uri": export_surface_loc.uri,
                "path": export_cand.path.as_posix(),
                "directory": export_cand.path.parent.as_posix(),
                "range": {
                    "start": {
                        "line0": export_surface_loc.start_line,
                        "col0": export_surface_loc.start_col,
                    },
                    "end": {
                        "line0": export_surface_loc.end_line,
                        "col0": export_surface_loc.end_col,
                    },
                },
                "full_def_source": export_src,
            }
            try:
                export_rel = export_cand.path.resolve().relative_to(repo_root.resolve())
                export_bundle["repo_relative_path"] = export_rel.as_posix()
                export_bundle["repo_relative_dir"] = export_rel.parent.as_posix()
            except Exception:
                pass
            bundle["export_surface"] = export_bundle
            if export_src and src:
                bundle["full_def_source"] = export_src.rstrip() + "\n\n" + src.lstrip()
            elif export_src:
                bundle["full_def_source"] = export_src

    return bundle


def _runtime_implementation_bundle_is_useful(
    bundle: Dict[str, Any],
    symbol_name: Optional[str],
) -> bool:
    """Reject generated-file headers and other runtime snippets that miss the symbol."""
    src = (bundle.get("full_def_source") or "").strip()
    if len(src) < 4:
        return False
    if symbol_name and not re.search(r"\b" + re.escape(symbol_name) + r"\b", src):
        return False
    head = "\n".join(src.splitlines()[:8]).lower()
    if "do not edit directly" in head and symbol_name:
        if not re.search(
            rf"\b(?:function|async\s+function|const|let|var|exports\.)\s*{re.escape(symbol_name)}\b",
            src,
        ):
            return False
    rng = bundle.get("range") or {}
    start = rng.get("start") or {}
    if (
        symbol_name
        and start.get("line0", 0) == 0
        and start.get("col0", 0) == 0
        and not re.search(
            rf"^\s*(?:export\s+)?(?:async\s+)?function\s+{re.escape(symbol_name)}\b",
            src,
            re.M,
        )
        and not re.search(rf"^\s*exports\.{re.escape(symbol_name)}\s*=", src, re.M)
    ):
        first_line = src.splitlines()[0].strip() if src else ""
        if not first_line or first_line.startswith("/*") or first_line.startswith("//"):
            return False
    return True


def _upgrade_external_declaration_runtime(
    client: GenericLSPClient,
    repo_root: Path,
    chosen_def: DefCandidate,
    full_def_source: Optional[str],
    symbol_name: Optional[str],
) -> Tuple[DefCandidate, Optional[str], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    If the chosen definition is an external .d.ts, try LSP implementation / maps / sibling JS.

    Returns ``(candidate, source, trace, runtime_implementation)``.
    The declaration/export surface stays primary; a concrete runtime body is attached
    separately in ``runtime_implementation`` when found.
    """
    if not chosen_def.is_d_ts or not chosen_def.in_node_modules:
        return chosen_def, full_def_source, None, None
    try:
        from ts_external_runtime_impl import (
            is_declaration_surface,
            should_attempt_external_runtime_resolution,
            symbol_located_in_file,
            try_resolve_external_runtime_implementation,
        )
    except ImportError:
        return chosen_def, full_def_source, None, None

    if not should_attempt_external_runtime_resolution(chosen_def.path, repo_root=repo_root):
        return chosen_def, full_def_source, None, None

    res = try_resolve_external_runtime_implementation(
        client=client,
        declaration_loc=chosen_def.loc,
        declaration_path=chosen_def.path,
        symbol_name=symbol_name,
    )
    if res is None:
        return chosen_def, full_def_source, None, None

    impl_loc = res.implementation_loc
    if impl_loc is None:
        surf_path = uri_to_path(res.loc.uri)
        if (
            surf_path.resolve() != chosen_def.path.resolve()
            and not is_declaration_surface(surf_path)
            and symbol_located_in_file(surf_path, res.loc, symbol_name)
        ):
            impl_loc = res.loc

    runtime_implementation: Optional[Dict[str, Any]] = None
    if impl_loc is not None:
        impl_path = uri_to_path(impl_loc.uri)
        if symbol_name and not symbol_located_in_file(impl_path, impl_loc, symbol_name):
            impl_loc = None
    if impl_loc is not None:
        export_surface_loc: Optional[Location] = None
        if res.implementation_loc is not None:
            surface_path = uri_to_path(res.loc.uri)
            impl_path = uri_to_path(impl_loc.uri)
            if surface_path.resolve() != impl_path.resolve():
                export_surface_loc = res.loc
        candidate_bundle = _build_runtime_implementation_bundle(
            repo_root,
            impl_loc,
            symbol_name,
            export_surface_loc=export_surface_loc,
        )
        if _runtime_implementation_bundle_is_useful(candidate_bundle, symbol_name):
            runtime_implementation = candidate_bundle

    trace: Dict[str, Any] = {"method": res.method, **res.trace}
    if runtime_implementation is not None:
        trace["implementation_path"] = runtime_implementation.get("path")
    elif res.method == "sibling_module":
        trace["note"] = "runtime_module_found_but_symbol_not_located"

    return chosen_def, full_def_source, trace, runtime_implementation


def _declaration_surface_snapshot_from_def(chosen_def: DefCandidate) -> Dict[str, Any]:
    return {
        "path": chosen_def.path.as_posix(),
        "uri": chosen_def.loc.uri,
        "range": {
            "start": {
                "line0": chosen_def.loc.start_line,
                "col0": chosen_def.loc.start_col,
            },
            "end": {
                "line0": chosen_def.loc.end_line,
                "col0": chosen_def.loc.end_col,
            },
        },
    }


def _try_external_declaration_runtime_upgrade(
    client: Optional[GenericLSPClient],
    repo_root: Path,
    chosen_def: DefCandidate,
    full_def_source: Optional[str],
    symbol_name: Optional[str],
) -> Tuple[bool, Optional[Dict[str, Any]], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Resolve runtime implementation for an external node_modules .d.ts definition.

    Returns ``(upgraded, declaration_surface, runtime_implementation, ext_trace)``.
    ``upgraded`` is True when ``ext_trace`` is not None.
    """
    if client is None or not chosen_def.is_d_ts or not chosen_def.in_node_modules:
        return False, None, None, None

    declaration_surface = _declaration_surface_snapshot_from_def(chosen_def)
    _, _, ext_trace, runtime_implementation = _upgrade_external_declaration_runtime(
        client,
        repo_root,
        chosen_def,
        full_def_source,
        symbol_name,
    )
    if ext_trace is None:
        return False, None, None, None
    return True, declaration_surface, runtime_implementation, ext_trace


def _build_outer_definition(
    *,
    chosen_def: DefCandidate,
    repo_root: Path,
    full_def_source: Optional[str],
    client: Optional[GenericLSPClient] = None,
    declaration_surface: Optional[Dict[str, Any]] = None,
    runtime_implementation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build the ``outer_definition`` payload from a chosen definition candidate."""
    loc = chosen_def.loc
    def_path = chosen_def.path
    outer: Dict[str, Any] = {**loc.to_json()}
    outer["path"] = def_path.as_posix()
    outer["directory"] = def_path.parent.as_posix()
    outer["full_def_source"] = full_def_source
    if declaration_surface is not None:
        outer["declaration_surface"] = declaration_surface
    if runtime_implementation is not None:
        outer["runtime_implementation"] = runtime_implementation
    if client is not None:
        try:
            outer["callee_documentation"] = client.hover(loc.uri, loc.start_line, loc.start_col)
        except Exception:
            outer["callee_documentation"] = None
    else:
        outer["callee_documentation"] = None
    try:
        rel = def_path.resolve().relative_to(repo_root.resolve())
        outer["repo_relative_path"] = rel.as_posix()
        outer["repo_relative_dir"] = rel.parent.as_posix()
    except Exception:
        pass
    return outer


def _definition_source_is_import_or_export(loc: Location, symbol_name: Optional[str]) -> bool:
    """True for import lines and export re-exports, not for real exported declarations."""
    from code_navigation_TypeScript import _read_definition_source

    src = _read_definition_source(loc, symbol_name)
    if not src:
        return False
    stripped = src.strip()
    if stripped.startswith("import "):
        return True
    if not stripped.startswith("export "):
        return False
    if re.match(
        r"^export\s+(?:default\s+)?(?:abstract\s+)?(?:class|interface|type|enum|function|const|let|var)\b",
        stripped,
    ):
        return False
    return True


def _definition_source_looks_like_usage(
    loc: Location,
    symbol_name: Optional[str],
    doc_uri: str,
    full_def_source: Optional[str],
) -> bool:
    """True if the definition source looks like a call site (e.g. symbol().should(...)), not a declaration.
    Used only as fallback when AST-based check is unavailable. Prefer _definition_location_is_call_site_ast."""
    if not symbol_name or not full_def_source or loc.uri != doc_uri:
        return False
    s = full_def_source.strip()
    if re.search(r"\.should\s*\(", s) or re.search(r"\.expect\s*\(", s):
        return True
    if "\n" not in s and not re.search(r"\b(?:export|function|const|let|var|class)\b", s):
        if re.match(r"\s*" + re.escape(symbol_name) + r"\s*\(", s):
            return True
    return False


def _find_definition_via_imports(
    script_path: Path,
    symbol_name: str,
    repo_root: Path,
) -> Optional[Tuple[Path, int]]:
    """
    When the LSP returned a usage, try to find the real definition by following imports.
    Returns (path, line_0based) of the export line, or None.
    """
    try:
        text = script_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    imp_re = re.compile(
        r"import\s+(?:\{[^}]*\b" + re.escape(symbol_name) + r"\b[^}]*\}|"
        r"\*\s+as\s+" + re.escape(symbol_name) + r"\b|"
        r"\b" + re.escape(symbol_name) + r"\b)\s+from\s+['\"]([^'\"]+)['\"]"
    )
    for m in imp_re.finditer(text):
        from_path_str = m.group(1)
        if from_path_str.startswith("."):
            resolved = (script_path.parent / from_path_str).resolve()
        else:
            continue
        if not resolved.exists():
            for ext in (".ts", ".tsx", ".mts", ".js", ".jsx", ".mjs"):
                with_ext = resolved.parent / (resolved.name + ext)
                if with_ext.exists():
                    resolved = with_ext
                    break
            else:
                continue
        try:
            resolved.resolve().relative_to(repo_root.resolve())
        except ValueError:
            continue
        try:
            export_text = resolved.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        lines = export_text.splitlines()
        export_re = re.compile(
            r"export\s+(?:const|function|async\s+function)\s+" + re.escape(symbol_name) + r"\b"
        )
        for i, line in enumerate(lines):
            if export_re.search(line):
                return (resolved, i)
    return None


def _location_has_implementation_body(loc: Location, symbol_name: Optional[str]) -> bool:
    """True if the source at this location looks like a method/function body (has `{`), not just a declaration."""
    from code_navigation_TypeScript import _read_definition_source

    src = _read_definition_source(loc, symbol_name)
    if not src or "{" not in src:
        return False
    if _definition_source_is_import_or_export(loc, symbol_name):
        return False
    return True


def _path_looks_like_test_file(path: Path) -> bool:
    p = path.as_posix().lower()
    return (
        "/__tests__/" in p
        or p.endswith(".test.ts")
        or p.endswith(".spec.ts")
        or p.endswith(".test.js")
        or p.endswith(".spec.js")
    )


def _definition_source_looks_like_declaration_site(loc: Location) -> bool:
    from code_navigation_TypeScript import _read_definition_source

    src = _read_definition_source(loc, None)
    if not src:
        return False
    s = src.strip()
    if not s:
        return False
    if re.search(r"\b(?:class|interface|type)\b", s):
        return True
    if re.search(r"\b(?:readonly\s+)?[A-Za-z_$][\w$]*\s*\??:\s*[A-Za-z_$]", s):
        return True
    if "@" in s and ":" in s and "{" not in s:
        return True
    return False


def _definition_source_matches_symbol(source: Optional[str], symbol_name: str) -> bool:
    """
    True if the definition source actually refers to the resolved symbol (e.g. method name).
    Uses word boundary so we reject type aliases (e.g. RejectFn for symbol 'reject')
    or wrong symbols (e.g. 'interface Array' for symbol 'getHighestNode').
    """
    if not source or not symbol_name:
        return True
    esc = re.escape(symbol_name)
    patterns = (
        rf"\bfunction\s+{esc}\b",
        rf"\b(?:class|interface|type|enum)\s+{esc}\b",
        rf"\b(?:const|let|var)\s+{esc}\b",
        rf"\b(?:exports|module\.exports)\.{esc}\s*=",
        rf"(^|\n)\s*(?:async\s+)?{esc}\s*\(",
        rf"(^|\n)\s*(?:async\s+)?{esc}\s*<",
        rf"(^|\n)\s*(?:public|private|protected|static|readonly|abstract|override|\s)*{esc}\s*\(",
        rf"(^|\n)\s*(?:public|private|protected|static|readonly|abstract|override|\s)*{esc}\s*<",
        rf"\b(?:get|set)\s+{esc}\s*\(",
        rf"\b{esc}\s*:\s*(?:function\b|\([^)]*\)\s*=>)",
        rf"\[\s*['\"]{esc}['\"]\s*\]\s*=",
        rf"\b{esc}\s*:\s*",
        rf"\b{esc}\s*\??\s*:\s*",
        rf"(^|\n)\s*{esc}\s*=\s*",
    )
    return any(re.search(p, source, re.M) for p in patterns)


def _choose_one_definition(
    repo_root: Path,
    locs: List[Location],
    symbol_name: Optional[str] = None,
    usage_kind: Optional[str] = None,
    prefer_same_document_uri: Optional[str] = None,
    preferred_locations: Optional[List[Location]] = None,
) -> Tuple[Optional[DefCandidate], Dict[str, Any]]:

    debug: Dict[str, Any] = {
        "policy": [
            "prefer_go_to_source_definition",
            "drop_d_ts",
            "prefer_repo_local",
            "prefer_non_node_modules",
            "prefer_implementation_over_declaration",
            "tie_break_shorter_path_then_position",
        ],
        "dropped": {"d_ts": []},
        "note": None,
        "ambiguity": None,
    }

    if not locs:
        debug["note"] = "no_definitions_from_lsp"
        return None, debug

    candidates = [_build_def_candidate(repo_root, loc) for loc in locs]

    if preferred_locations:
        pref_keys = {
            (loc.uri, loc.start_line, loc.start_col, loc.end_line, loc.end_col)
            for loc in preferred_locations
        }
        preferred_cands = [
            c
            for c in candidates
            if (c.loc.uri, c.loc.start_line, c.loc.start_col, c.loc.end_line, c.loc.end_col)
            in pref_keys
        ]
        if preferred_cands:
            candidates = preferred_cands
            debug["note"] = "preferred_go_to_source_definition"

    non_dts = [c for c in candidates if not c.is_d_ts]
    debug["dropped"]["d_ts"] = [c.path.as_posix() for c in candidates if c.is_d_ts]
    if non_dts:
        pool = non_dts
        debug["note"] = "d_ts_dropped_if_possible"
    else:
        pool = candidates
        debug["note"] = "only_d_ts_available"

    repo_local = [c for c in pool if c.is_repo_local]
    if repo_local:
        pool = repo_local
        debug["note"] = f"preferred_repo_local_kept={len(pool)}"

    non_node_modules = [c for c in pool if not c.in_node_modules]
    if non_node_modules:
        pool = non_node_modules
        debug["note"] = f"preferred_non_node_modules_kept={len(pool)}"

    non_test = [c for c in pool if not _path_looks_like_test_file(c.path)]
    if non_test:
        pool = non_test
        debug["note"] = f"preferred_non_test_files_kept={len(pool)}"

    if prefer_same_document_uri and usage_kind == "attr":
        same_doc = [c for c in pool if c.loc.uri == prefer_same_document_uri]
        if same_doc:
            pool = same_doc
            debug["note"] = f"{debug['note']}; prefer_usage_document_uri"

    if symbol_name:
        non_import_export = [
            c for c in pool if not _definition_source_is_import_or_export(c.loc, symbol_name)
        ]
        if non_import_export:
            pool = non_import_export
            debug["note"] = f"dropped_import_export_sites_kept={len(pool)}"
    elif len(pool) > 1:
        declaration_like = [c for c in pool if _definition_source_looks_like_declaration_site(c.loc)]
        if declaration_like:
            pool = declaration_like
            debug["note"] = f"preferred_declaration_like_sites_kept={len(pool)}"

    if symbol_name and usage_kind == "call" and len(pool) > 1:
        with_body = [c for c in pool if _location_has_implementation_body(c.loc, symbol_name)]
        if with_body:
            pool = with_body
            debug["note"] = f"preferred_implementation_over_declaration_kept={len(pool)}"

    pool_sorted = sorted(
        pool,
        key=lambda c: (c.path_len, c.path.as_posix(), c.loc.start_line, c.loc.start_col),
    )
    chosen = pool_sorted[0]

    if len(pool_sorted) > 1:
        debug["ambiguity"] = {
            "remaining": len(pool_sorted),
            "chosen": chosen.path.as_posix(),
            "others": [c.path.as_posix() for c in pool_sorted[1:]],
        }
    else:
        debug["ambiguity"] = {"remaining": 1}

    return chosen, debug


def _nested_usages_in_snippet(snippet: str, outer_name: str) -> List[Dict[str, Any]]:

    out: List[Dict[str, Any]] = []

    attr_re = re.compile(r"([A-Za-z_$][A-Za-z0-9_$]*)\s*\.\s*([A-Za-z_$][A-Za-z0-9_$]*)")
    for m in attr_re.finditer(snippet):
        recv, nm = m.group(1), m.group(2)
        if nm == outer_name and m.start(2) == snippet.find(outer_name):
            continue
        out.append(
            {
                "kind": "attr",
                "name": nm,
                "receiver": recv,
                "offset": m.start(2),
                "pattern": "nested_attr",
            }
        )

    call_re = re.compile(r"\b([A-Za-z_$][A-Za-z0-9_$]*)\s*\(")
    for m in call_re.finditer(snippet):
        nm = m.group(1)
        if nm == outer_name and m.start(1) == snippet.find(outer_name):
            continue
        out.append(
            {
                "kind": "call",
                "name": nm,
                "receiver": None,
                "offset": m.start(1),
                "pattern": "nested_bare_call",
            }
        )

    seen = set()
    uniq: List[Dict[str, Any]] = []
    for u in out:
        k = (u["kind"], u["name"], u["offset"])
        if k not in seen:
            seen.add(k)
            uniq.append(u)
    return uniq
