from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from lsp_client import GenericLSPClient, Location, file_uri, uri_to_path
from models import SnippetSelector
from ts_prepare_resolution import (
    nearest_tsconfig_dir,
    prepare_resolution,
    ts_server_cmd as _ts_server_cmd,
    ts_workspace_folder_uris,
)

# AST-based callee finding uses py-tree-sitter with the official grammar packages:
#   pip install tree-sitter tree-sitter-typescript tree-sitter-javascript
# Falls back to the older all-in-one tree-sitter-languages package on Python < 3.13.
try:
    from tree_sitter import Language, Parser
    import tree_sitter_typescript as _tsts
    import tree_sitter_javascript as _tsjs

    _TS_LANGUAGE_FACTORIES = {
        "typescript": lambda: Language(_tsts.language_typescript()),
        "tsx": lambda: Language(_tsts.language_tsx()),
        "javascript": lambda: Language(_tsjs.language()),
    }
    _TS_PARSER_CACHE: Dict[str, Any] = {}

    def get_parser(name: str):
        parser = _TS_PARSER_CACHE.get(name)
        if parser is None:
            parser = Parser(_TS_LANGUAGE_FACTORIES[name]())
            _TS_PARSER_CACHE[name] = parser
        return parser

    _TREE_SITTER_AVAILABLE = True
except ImportError:
    try:
        from tree_sitter_languages import get_parser
        _TREE_SITTER_AVAILABLE = True
    except ImportError:
        _TREE_SITTER_AVAILABLE = False


# Cache of long-lived TypeScript LSP clients so we don't spawn a new
# typescript-language-server process for every single callee. Keyed by
# (language_id, workspace_folder_uris...).
_TS_LSP_CLIENTS: Dict[Tuple[Any, ...], GenericLSPClient] = {}


def _ts_lsp_client_cache_key(repo_root: Path, script_path: Path, lang_id: str) -> Tuple[Any, ...]:
    folders = ts_workspace_folder_uris(repo_root, script_path)
    return (lang_id,) + tuple(folders)


def _is_comment_line(line: str) -> bool:
    s = line.strip()
    return s.startswith("//") or s.startswith("*") or s.startswith("/*") or s.startswith("* ")


def _get_preceding_jsdoc(lines: List[str], definition_start_line: int) -> str:
    """Return the block of comment/JSDoc lines immediately above the definition line (in top-to-bottom order)."""
    if definition_start_line <= 0:
        return ""
    collected: List[str] = []
    for i in range(definition_start_line - 1, -1, -1):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            collected.append(line)
            continue
        if _is_comment_line(line) or stripped.startswith("*/"):
            collected.append(line)
            continue
        break
    collected.reverse()
    return "\n".join(collected).strip()


def _append_preceding_jsdoc_to_snippet(
    lines: List[str], snippet: str, definition_line0: int
) -> str:
    """Prepend immediate JSDoc / comment block above definition_line0 (0-based)."""
    pre = _get_preceding_jsdoc(lines, definition_line0)
    if not pre:
        return snippet
    return pre + "\n" + snippet


def _is_ts_iface_body_comment_or_blank(line: str) -> bool:
    s = line.lstrip()
    return (
        not s
        or s.startswith("//")
        or s.startswith("*")
        or s.startswith("/*")
        or s.startswith("*/")
    )


def _ts_iface_member_decl_name(s: str) -> Optional[str]:
    """If s starts a method-like member `name<` or `name(`, return name; else None."""
    m = re.match(r"^([A-Za-z_$][\w$]*)\s*[\(<]", s)
    return m.group(1) if m else None


def _looks_ts_iface_property_line(s: str) -> bool:
    if re.match(r"^readonly\s+[A-Za-z_$][\w$]*\s*\??:", s):
        return True
    if re.match(r"^[A-Za-z_$][\w$]*\s*\??:", s):
        return True
    return False


def _extract_ts_symbol_definition(
    lines: List[str],
    symbol_name: str,
    hint_line0: int,
) -> Tuple[Optional[str], Optional[int]]:
    """
    Extract callable/method signature and body starting at symbol_name.
    Returns (source_text, first_line_0based) or (None, None).
    The line index is for the declaration's first line (e.g. `async foo(`), used to attach JSDoc.
    """

    if not symbol_name:
        return None, None

    # Require the symbol to start a callable member: `name(` or `name<`, not
    # `obj.name(...` (otherwise `this.logger.info` wins for symbol `logger`).
    name_re = re.compile(
        r"(?<!\.)\b" + re.escape(symbol_name) + r"\b\s*[\(<]"
    )

    candidate_lines: List[int] = []
    for i, line in enumerate(lines):
        if name_re.search(line):
            candidate_lines.append(i)

    if not candidate_lines:
        return None, None

    # Prefer the candidate closest to the location hinted by the LSP.
    start_idx = min(candidate_lines, key=lambda i: abs(i - hint_line0))
    base_line = lines[start_idx]
    base_indent = len(base_line) - len(base_line.lstrip())

    same_overload = re.compile(r"^" + re.escape(symbol_name) + r"\b\s*[<(]")

    def _foreign_jsdoc_before_other_member(start_i: int) -> Optional[int]:
        """
        If lines[start_i] opens a JSDoc block at base_indent that documents the next
        sibling member (different name than symbol_name), return the line index of the
        closing '*/' line so the caller can skip through it. Otherwise None.
        """
        if start_i >= len(lines):
            return None
        L0 = lines[start_i]
        if (len(L0) - len(L0.lstrip())) != base_indent or not L0.lstrip().startswith("/**"):
            return None
        j = start_i
        close_j: Optional[int] = None
        while j < len(lines):
            if "*/" in lines[j]:
                close_j = j
                break
            j += 1
        if close_j is None:
            return None
        k = close_j + 1
        while k < len(lines):
            L = lines[k]
            t = L.lstrip()
            ki = len(L) - len(L.lstrip())
            if not t or _is_ts_iface_body_comment_or_blank(L):
                k += 1
                continue
            if ki != base_indent:
                k += 1
                continue
            if same_overload.match(t) or t.startswith(")"):
                return None
            if _looks_ts_iface_property_line(t) or t.startswith("}"):
                return None
            other = _ts_iface_member_decl_name(t)
            if other is not None and other != symbol_name:
                return close_j
            return None
        return None

    snippet: List[str] = []
    i = start_idx
    while i < len(lines):
        line = lines[i]

        if i > start_idx:
            cur_indent = len(line) - len(line.lstrip())
            if cur_indent == base_indent:
                s = line.lstrip()
                skip_to = _foreign_jsdoc_before_other_member(i)
                if skip_to is not None:
                    i = skip_to + 1
                    continue
                if s and not _is_ts_iface_body_comment_or_blank(line):
                    if same_overload.match(s):
                        pass
                    elif s.startswith(")"):
                        # Multiline signature return line, e.g. `    ): Chainable<R>`
                        pass
                    elif _looks_ts_iface_property_line(s) or (
                        s.startswith("}")
                        # `}): Promise<T>;` closes a multiline function signature, not a class
                        and not re.search(r"}\s*\)\s*:", s)
                        and not s.rstrip().endswith(");")
                    ):
                        break
                    else:
                        other = _ts_iface_member_decl_name(s)
                        if other is not None and other != symbol_name:
                            break

        snippet.append(line)
        paren, brace = _delimiter_depths("\n".join(snippet))
        if paren == 0 and brace == 0 and line.rstrip().endswith(";"):
            # Keep collecting consecutive overload signatures at the same indent.
            if i + 1 < len(lines):
                nxt = lines[i + 1]
                nxt_indent = len(nxt) - len(nxt.lstrip())
                nxt_stripped = nxt.lstrip()
                if (
                    nxt_indent == base_indent
                    and nxt_stripped
                    and same_overload.match(nxt_stripped)
                ):
                    i += 1
                    continue
            break
        i += 1

    if not snippet:
        return None, None
    return "\n".join(snippet), start_idx


def _symbol_identifier_pattern(symbol_name: str) -> str:
    """Word-boundary match that respects `$foo` vs `foo` (e.g. Prisma `$transaction`)."""
    esc = re.escape(symbol_name)
    if symbol_name.startswith("$"):
        return rf"(?<![\w$]){esc}(?![\w$])"
    return rf"(?<![\w$\.]){esc}(?![\w$])"


def _symbol_decl_line_re(symbol_name: str) -> re.Pattern[str]:
    return re.compile(_symbol_identifier_pattern(symbol_name) + r"\s*[\(<]")


def _is_completed_declaration_line(line: str) -> bool:
    s = line.strip()
    if not s or _is_comment_line(line):
        return False
    return s.endswith(";") or (s.endswith("}") and "{" not in s)


def _first_call_arg_introducer(usage_hint: Optional[str]) -> Optional[str]:
    """Return the first argument token from a call-site snippet, if any."""
    if not usage_hint or "(" not in usage_hint:
        return None
    open_paren = usage_hint.find("(")
    close = usage_hint.find(")", open_paren + 1)
    if close == -1:
        inner = usage_hint[open_paren + 1 :].strip()
    else:
        inner = usage_hint[open_paren + 1 : close].strip()
    if not inner or inner == "...":
        return None
    return inner.split(None, 1)[0] if inner else None


def _pick_overload_index_for_usage(
    lines: List[str],
    symbol_name: str,
    overload_indices: List[int],
    hint_line0: int,
    usage_hint: Optional[str] = None,
) -> int:
    if len(overload_indices) <= 1:
        return overload_indices[0]
    first_arg = _first_call_arg_introducer(usage_hint)
    if first_arg in ("async", "function"):
        for idx in overload_indices:
            if re.search(r"\bfn\s*:\s*\(", lines[idx]):
                return idx
    if first_arg == "[":
        for idx in overload_indices:
            if "[]" in lines[idx] or "[...P]" in lines[idx]:
                return idx
    return min(overload_indices, key=lambda i: abs(i - hint_line0))


def _extract_ts_enum_member_definition(
    lines: List[str],
    symbol_name: str,
    hint_line0: int,
) -> Tuple[Optional[str], Optional[int]]:
    if not symbol_name:
        return None, None
    member_re = re.compile(
        r"^\s*" + re.escape(symbol_name) + r"\s*=\s*.+?,?\s*$"
    )
    candidates = [i for i, line in enumerate(lines) if member_re.match(line)]
    if not candidates:
        return None, None
    idx = min(candidates, key=lambda i: abs(i - hint_line0))
    return lines[idx].strip(), idx


def _merge_adjacent_callable_overloads(
    lines: List[str],
    symbol_name: str,
    hint_line0: int,
    snippet: str,
    start_idx: int,
) -> Tuple[str, int]:
    """
    When LSP lands on one overload, also include earlier/later overload signatures
    at the same member indent (common in .d.ts class interfaces).
    """
    if not symbol_name or not snippet:
        return snippet, start_idx

    same_overload = re.compile(
        r"^" + _symbol_identifier_pattern(symbol_name) + r"\s*[\(<]"
    )
    name_re = _symbol_decl_line_re(symbol_name)
    base_indent = len(lines[start_idx]) - len(lines[start_idx].lstrip())

    overload_indices = [
        i
        for i, line in enumerate(lines)
        if (len(line) - len(line.lstrip())) == base_indent
        and name_re.search(line)
        and same_overload.match(line.lstrip())
    ]
    if len(overload_indices) <= 1:
        return snippet, start_idx

    nearest = min(overload_indices, key=lambda i: abs(i - hint_line0))
    group = [nearest]
    for i in sorted(overload_indices):
        if i == nearest:
            continue
        if any(abs(i - g) <= 3 for g in group):
            group.append(i)
    group = sorted(set(group))
    if len(group) <= 1:
        return snippet, start_idx

    merged_start = min(group)
    part, part_start = _extract_ts_symbol_definition(
        lines, symbol_name, merged_start
    )
    if not part:
        return snippet, start_idx
    if part_start is None:
        part_start = merged_start
    if part.strip() == snippet.strip():
        return snippet, start_idx
    return part, part_start


def _extract_ts_property_definition(
    lines: List[str],
    symbol_name: str,
    hint_line0: int,
) -> Optional[str]:
    if not symbol_name:
        return None
    # Constructor params / fields: `private readonly logger: Logger`, `public x?: T`, or `name: T`.
    prop_re = re.compile(
        r"^\s*(?:(?:public|private|protected|static|abstract|override|declare|readonly)\s+)*"
        + re.escape(symbol_name)
        + r"\s*\??\s*:"
    )
    ctor_param_re = re.compile(
        r"\b(?:public|private|protected)\s+(?:readonly\s+)?"
        + re.escape(symbol_name)
        + r"\s*\??\s*:"
    )
    field_init_re = re.compile(
        r"^\s*(?:(?:public|private|protected|static|readonly)\s+)*"
        + re.escape(symbol_name)
        + r"\s*="
    )
    candidates = [
        i for i, line in enumerate(lines)
        if prop_re.search(line) or ctor_param_re.search(line) or field_init_re.search(line)
    ]
    if not candidates:
        return None
    idx = min(candidates, key=lambda i: abs(i - hint_line0))
    start = idx
    while start > 0:
        prev = lines[start - 1].strip()
        if prev.startswith("@") or prev.startswith("//") or prev.startswith("/*") or prev.startswith("*") or prev == "":
            start -= 1
            continue
        break
    return "\n".join(lines[start:idx + 1]).strip()


def _extract_symbol_definition_ast(
    path: Path,
    symbol_name: str,
    hint_line0: int,
) -> Tuple[Optional[str], Optional[int]]:
    """
    AST-first symbol extraction for JS/TS files.
    Returns (snippet, start_line0) for declaration-like nodes only.
    """
    if not symbol_name:
        return None, None
    parser = _get_ts_parser(path)
    if parser is None:
        return None, None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None, None
    lines = text.splitlines()
    source_bytes = text.encode("utf-8")
    try:
        tree = parser.parse(source_bytes)
    except Exception:
        return None, None
    if tree.root_node is None or tree.root_node.has_error:
        return None, None

    candidates: List[Tuple[int, int, int, int]] = []

    def _node_src(node) -> str:
        return _node_text(source_bytes, node)

    def _push(node) -> None:
        if node is None:
            return
        sl, sc = node.start_point
        el, ec = node.end_point
        candidates.append((int(sl), int(sc), int(el), int(ec)))

    def walk(node) -> None:
        # function foo() / method foo()
        if node.type in ("function_declaration", "method_definition"):
            name_node = node.child_by_field_name("name")
            if name_node is not None and _node_src(name_node) == symbol_name:
                _push(node)

        # const/let/var foo = ...
        if node.type in ("lexical_declaration", "variable_declaration"):
            for i in range(node.child_count):
                child = node.child(i)
                if child.type != "variable_declarator":
                    continue
                name_node = child.child_by_field_name("name")
                if name_node is not None and _node_src(name_node) == symbol_name:
                    _push(child)

        # exports.foo = ... / module.exports.foo = ...
        if node.type == "assignment_expression":
            left = node.child_by_field_name("left")
            if left is not None and left.type == "member_expression":
                prop = left.child_by_field_name("property")
                if prop is not None and _node_src(prop) == symbol_name:
                    obj = left.child_by_field_name("object")
                    obj_src = _node_src(obj).strip() if obj is not None else ""
                    if obj_src in ("exports", "module.exports"):
                        _push(node)

        for i in range(node.child_count):
            walk(node.child(i))

    walk(tree.root_node)
    if not candidates:
        return None, None

    # Prefer declaration nearest to hinted LSP line.
    sl, _sc, el, _ec = min(candidates, key=lambda t: abs(t[0] - hint_line0))
    start = max(0, sl)
    end = min(len(lines), max(el + 1, start + 1))
    if start >= end:
        return None, None
    return "\n".join(lines[start:end]), start


def _extract_ts_class_or_interface(
    lines: List[str],
    symbol_name: str,
    hint_line0: int,
) -> Optional[str]:
    """Extract full class or interface body"""
    if not symbol_name:
        return None
    # Match "class Name " or "interface Name "
    class_re = re.compile(
        r"\b(?:export\s+)?(?:abstract\s+)?(?:class|interface)\s+"
        + re.escape(symbol_name)
        + r"\b"
    )
    candidate_lines: List[int] = []
    for i, line in enumerate(lines):
        if class_re.search(line):
            candidate_lines.append(i)
    if not candidate_lines:
        return None
    start_idx = min(candidate_lines, key=lambda i: abs(i - hint_line0))
    i = start_idx
    brace_depth = 0
    saw_brace = False
    snippet: List[str] = []
    while i < len(lines):
        line = lines[i]
        snippet.append(line)
        for ch in line:
            if ch == "{":
                brace_depth += 1
                saw_brace = True
            elif ch == "}":
                if brace_depth > 0:
                    brace_depth -= 1
        if saw_brace and brace_depth == 0:
            break
        i += 1
    return "\n".join(snippet) if snippet else None


def _get_referenced_type_on_line(line: str) -> Optional[Tuple[str, int]]:
    """
    If line looks like a declaration with a type (e.g. '  name: TypeName;'),
    return (TypeName, character_offset_of_TypeName). Otherwise None.
    """
    # Match ": TypeName" or ": TypeName;" or ": TypeName<...>"
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
    # Return type of constructor: "): Date;" or "): Array;" etc.
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


# When LSP already returns a tight, self-contained declaration, do not widen it.
_LSP_RANGE_MAX_TRUST_LINES = 30


def _lsp_range_line_span(loc: Location) -> int:
    if loc.end_line < loc.start_line:
        return 1
    return loc.end_line - loc.start_line + 1


def _snippet_from_lsp_range(lines: List[str], loc: Location) -> Tuple[str, int]:
    start = max(0, loc.start_line)
    end = min(len(lines), loc.end_line + 1)
    if end <= start:
        line0 = max(0, min(loc.start_line, len(lines) - 1))
        return lines[line0], line0
    return "\n".join(lines[start:end]), start


def _delimiter_depths(text: str) -> Tuple[int, int]:
    """Return (paren_depth, brace_depth) after scanning text (strings ignored)."""
    paren = brace = 0
    for ch in text:
        if ch == "(":
            paren += 1
        elif ch == ")":
            paren -= 1
        elif ch == "{":
            brace += 1
        elif ch == "}":
            brace -= 1
    return paren, brace


def _extend_declaration_end_line(
    lines: List[str],
    decl_line0: int,
    *,
    max_lines: int = 40,
) -> int:
    """
    From a declaration line (e.g. export function foo(), extend through multiline
    signatures ending in `;` or a closed `{...}` body.
    """
    paren = brace = 0
    last_i = decl_line0
    for i in range(decl_line0, min(len(lines), decl_line0 + max_lines)):
        line = lines[i]
        last_i = i
        for ch in line:
            if ch == "(":
                paren += 1
            elif ch == ")":
                paren -= 1
            elif ch == "{":
                brace += 1
            elif ch == "}":
                brace -= 1
        stripped = line.rstrip()
        if paren == 0 and brace == 0 and stripped.endswith(";"):
            return i
        if paren == 0 and brace == 0 and stripped.endswith("}") and i > decl_line0:
            return i
        # `.d.ts` callable signatures often end with `>` / `)` without a trailing `;`.
        if paren == 0 and brace == 0 and i >= decl_line0:
            if re.search(r"\)\s*(?::\s*[^;{]+)?\s*$", stripped):
                return i
            if re.search(r">\s*$", stripped) and "(" in stripped:
                return i
    return last_i


def _lsp_range_is_complete_declaration(
    lines: List[str],
    loc: Location,
    symbol_name: Optional[str] = None,
) -> bool:
    """
    True when textDocument/definition range already spans a full
    declaration. In that case we trust the range and skip heuristic wideners that
    can swallow sibling lib globals
    """
    if _lsp_range_line_span(loc) > _LSP_RANGE_MAX_TRUST_LINES:
        return False
    start = max(0, loc.start_line)
    end = min(len(lines), loc.end_line + 1)
    chunk_lines = (
        lines[start:end]
        if end > start
        else ([lines[loc.start_line]] if 0 <= loc.start_line < len(lines) else [])
    )
    chunk = "\n".join(chunk_lines)
    if not chunk.strip():
        return False
    if symbol_name and not re.search(_symbol_identifier_pattern(symbol_name), chunk):
        return False
    non_comment = [
        ln
        for ln in chunk_lines
        if ln.strip() and not _is_comment_line(ln) and not ln.strip().startswith("*/")
    ]
    if not non_comment:
        return False
    if symbol_name and len(non_comment) > 1:
        sym_pat = _symbol_identifier_pattern(symbol_name)
        sym_lines = [ln for ln in non_comment if re.search(sym_pat, ln)]
        if len(sym_lines) == 1 and len(non_comment) > len(sym_lines):
            return False
        decl_re = _symbol_decl_line_re(symbol_name)
        for ln in non_comment:
            if _is_completed_declaration_line(ln) and not decl_re.search(ln):
                return False
        enum_member_lines = [
            ln for ln in non_comment if re.match(r"^\s*\w+\s*=\s*.+,?\s*$", ln)
        ]
        if len(enum_member_lines) > 1:
            return False
    paren, brace = _delimiter_depths(chunk)
    if paren != 0 or brace != 0:
        return False
    last = non_comment[-1].rstrip()
    if last.endswith(";"):
        return True
    if "{" in chunk and last.endswith("}"):
        return True
    return False


def _trim_trusted_lsp_snippet_to_symbol(
    lines: List[str],
    loc: Location,
    symbol_name: str,
    *,
    usage_hint: Optional[str] = None,
) -> Tuple[str, int]:
    """
    When a tight LSP range still spans multiple top-level declarations (common in
    lib*.d.ts), keep only the JSDoc + declaration for symbol_name.
    """
    decl_re = _symbol_decl_line_re(symbol_name)
    search_start = max(0, loc.start_line - 15)
    search_end = min(len(lines), loc.end_line + 25)
    decl_indices = [
        i
        for i in range(search_start, search_end)
        if decl_re.search(lines[i]) and not _is_comment_line(lines[i])
    ]
    if not decl_indices:
        start = max(0, loc.start_line)
        end = min(len(lines), loc.end_line + 1)
        chunk_lines = lines[start:end] if end > start else [lines[loc.start_line]]
        for i, ln in enumerate(chunk_lines):
            if decl_re.search(ln) and not _is_comment_line(ln):
                decl_indices = [start + i]
                break
    if not decl_indices:
        return _snippet_from_lsp_range(lines, loc)

    collapsed_usage = bool(
        usage_hint and re.search(r"\(\s*\.\.\.\s*\)", usage_hint)
    )
    if collapsed_usage and len(decl_indices) > 1:
        base_indent = len(lines[decl_indices[0]]) - len(lines[decl_indices[0]].lstrip())
        decl_indices = [
            i
            for i in decl_indices
            if (len(lines[i]) - len(lines[i].lstrip())) == base_indent
        ]
        abs_decl = min(decl_indices)
        end_line0 = max(
            _extend_declaration_end_line(lines, i) for i in decl_indices
        )
    else:
        abs_decl = _pick_overload_index_for_usage(
            lines, symbol_name, decl_indices, loc.start_line, usage_hint
        )
        end_line0 = _extend_declaration_end_line(lines, abs_decl)

    js_start = abs_decl
    for j in range(abs_decl - 1, search_start - 1, -1):
        line = lines[j]
        t = line.strip()
        if not t or _is_comment_line(line) or t.startswith("*/"):
            js_start = j
            continue
        if _is_completed_declaration_line(line):
            break
        break
    for i in range(js_start, abs_decl):
        line = lines[i]
        if (
            _is_completed_declaration_line(line)
            and not decl_re.search(line)
        ):
            js_start = i + 1
    trimmed = lines[js_start : end_line0 + 1]
    return "\n".join(trimmed), js_start


def _read_definition_source(
    loc: Location,
    symbol_name: Optional[str] = None,
    *,
    usage_hint: Optional[str] = None,
) -> Optional[str]:

    try:
        p = uri_to_path(loc.uri)
        if not p.exists():
            return None
        text = p.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        try:
            from ts_external_runtime_impl import is_declaration_surface as _is_decl_surface
        except ImportError:
            _is_decl_surface = lambda path: path.name.endswith(".d.ts")  # type: ignore[assignment]

        def _prepend_jsdoc(snippet: str, start_line: int) -> str:
            return _append_preceding_jsdoc_to_snippet(lines, snippet, start_line)

        if symbol_name:
            enum_snippet, enum_line = _extract_ts_enum_member_definition(
                lines, symbol_name, loc.start_line
            )
            if enum_snippet is not None and enum_line is not None:
                if abs(enum_line - loc.start_line) <= 5:
                    return enum_snippet

        if _lsp_range_is_complete_declaration(lines, loc, symbol_name):
            if symbol_name:
                body, body_line = _trim_trusted_lsp_snippet_to_symbol(
                    lines, loc, symbol_name, usage_hint=usage_hint
                )
            else:
                body, body_line = _snippet_from_lsp_range(lines, loc)
            if (
                symbol_name
                and _is_decl_surface(p)
                and body
                and body_line is not None
            ):
                body, body_line = _merge_adjacent_callable_overloads(
                    lines, symbol_name, loc.start_line, body, body_line
                )
            if "/**" in body or body.lstrip().startswith("//"):
                return body
            return _prepend_jsdoc(body, body_line)

        if symbol_name:
            ast_snippet, ast_start = _extract_symbol_definition_ast(
                p, symbol_name, loc.start_line
            )
            if ast_snippet is not None and ast_start is not None:
                return _prepend_jsdoc(ast_snippet, ast_start)
            if p.suffix.lower() in (".js", ".jsx", ".mjs", ".cjs"):
                esc = re.escape(symbol_name)
                js_decl_patterns = (
                    rf"^\s*(?:export\s+)?(?:async\s+)?function\s+{esc}\b",
                    rf"^\s*(?:export\s+)?(?:const|let|var)\s+{esc}\b",
                    rf"^\s*(?:exports|module\.exports)\.{esc}\s*=",
                    rf"^\s*(?:export\s+)?{esc}\s*:\s*(?:function\b|\([^)]*\)\s*=>)",
                    rf"^\s*(?:async\s+)?{esc}\s*\(",
                    rf"^\s*(?:public|private|protected|static|readonly|abstract|override|declare)\s+(?:async\s+)?{esc}\b\s*[\(<]",
                    rf"\[\s*['\"]{esc}['\"]\s*\]\s*=",
                )
                js_candidates = [
                    i for i, line in enumerate(lines)
                    if any(re.search(pat, line) for pat in js_decl_patterns)
                ]
                if js_candidates:
                    idx = min(js_candidates, key=lambda i: abs(i - loc.start_line))
                    snippet, sym_start = _extract_ts_symbol_definition(
                        lines, symbol_name, idx
                    )
                    if snippet is not None and sym_start is not None:
                        return _prepend_jsdoc(snippet, sym_start)
                    return _prepend_jsdoc(lines[idx], idx)
            # `export declare const foo:` / `const foo:` (e.g. fp-ts `left`, `right` in .d.ts).
            # Run before _extract_ts_symbol_definition: otherwise `left(` inside JSDoc examples
            # wins over the real `const left:` line when the symbol name is a common word.
            const_decl_re = re.compile(
                r"(?<!\.)(?:export\s+)?(?:declare\s+)?const\s+"
                + re.escape(symbol_name)
                + r"\b\s*:"
            )
            const_line_idxs = [i for i, line in enumerate(lines) if const_decl_re.search(line)]
            if const_line_idxs:
                idx = min(const_line_idxs, key=lambda i: abs(i - loc.start_line))
                if abs(idx - loc.start_line) <= 5:
                    return _prepend_jsdoc(lines[idx], idx)
            snippet, sym_start = _extract_ts_symbol_definition(lines, symbol_name, loc.start_line)
            if snippet is not None and sym_start is not None:
                paren, brace = _delimiter_depths(snippet)
                if paren != 0 or brace != 0:
                    end_line0 = _extend_declaration_end_line(lines, sym_start)
                    snippet = "\n".join(lines[sym_start : end_line0 + 1])
                if _is_decl_surface(p):
                    snippet, sym_start = _merge_adjacent_callable_overloads(
                        lines, symbol_name, loc.start_line, snippet, sym_start
                    )
                return _prepend_jsdoc(snippet, sym_start)
            if const_line_idxs:
                idx = min(const_line_idxs, key=lambda i: abs(i - loc.start_line))
                return _prepend_jsdoc(lines[idx], idx)
            snippet = _extract_ts_property_definition(lines, symbol_name, loc.start_line)
            if snippet:
                field_re = re.compile(
                    r"^\s*(?:(?:public|private|protected|static|readonly)\s+)*"
                    + re.escape(symbol_name)
                    + r"\s*="
                )
                prop_candidates = [
                    i for i, line in enumerate(lines) if field_re.search(line)
                ]
                start_line = (
                    min(prop_candidates, key=lambda i: abs(i - loc.start_line))
                    if prop_candidates
                    else loc.start_line
                )
                return _prepend_jsdoc(snippet, start_line)
            snippet = _extract_ts_class_or_interface(lines, symbol_name, loc.start_line)
            if snippet:
                # When we got the instance interface (e.g. Date with many methods) but the user
                # asked for the callable (Date()), prefer the FooConstructor snippet.
                if (
                    "new (" not in snippet
                    and re.search(r"\)\s*:\s*\w+\s*;", snippet)
                ):
                    constructor_snippet = _find_constructor_snippet(lines, symbol_name)
                    if constructor_snippet:
                        return constructor_snippet
                return _prepend_jsdoc(snippet, loc.start_line)

        # include all lines covered by LSP range; expand to full symbol body when possible.
        start = max(0, loc.start_line)
        end = min(len(lines), loc.end_line + 1)
        if start >= end:
            if 0 <= loc.start_line < len(lines):
                body = lines[loc.start_line]
                body_line = loc.start_line
            else:
                return None
        else:
            body = "\n".join(lines[start:end])
            body_line = start

        if symbol_name and ("{" in body or body.rstrip().endswith("{")):
            if not _lsp_range_is_complete_declaration(lines, loc, symbol_name):
                expanded, exp_start = _extract_ts_symbol_definition(
                    lines, symbol_name, loc.start_line
                )
                if expanded is not None and exp_start is not None and len(expanded) > len(body):
                    return _prepend_jsdoc(expanded, exp_start)

        # When LSP returned an instance-method snippet (e.g. setUTCFullYear for Date()) but the
        # user asked for the callable (constructor), prefer the FooConstructor interface.
        # Applies to any TS lib global: Date, Array, Map, Set, Promise, Object, RegExp, etc.
        if (
            symbol_name
            and "new (" not in body
            and re.search(r"\)\s*:\s*\w+\s*;", body)
        ):
            constructor_snippet = _find_constructor_snippet(lines, symbol_name)
            if constructor_snippet:
                return constructor_snippet
        if symbol_name:
            trimmed, trim_start = _trim_trusted_lsp_snippet_to_symbol(
                lines, loc, symbol_name, usage_hint=usage_hint
            )
            if trimmed and re.search(_symbol_identifier_pattern(symbol_name), trimmed):
                if _is_decl_surface(p):
                    trimmed, trim_start = _merge_adjacent_callable_overloads(
                        lines, symbol_name, loc.start_line, trimmed, trim_start
                    )
                if "/**" in trimmed or trimmed.lstrip().startswith("//"):
                    return trimmed
                return _prepend_jsdoc(trimmed, trim_start)
        return _prepend_jsdoc(body, body_line)
    except Exception:
        return None

def _expr_src_offset_for_selector_name(expr_src: str, selector: SnippetSelector) -> int:
    """
    Byte/character offset from the start of expr_src to the callee identifier.
    Naive .find(name) is wrong when name is a prefix of another segment (e.g. `error`
    inside `this.errorReporter.error(...)`).
    For multiline callees, prefer `receiver.name` so we do not pick a nested `.forEach`
    / `.error` inside the callback body.
    """
    name = selector.name
    if not name:
        return 0
    esc = re.escape(name)
    recv = (selector.receiver or "").strip()
    if recv:
        needle = recv + "." + name
        pos = expr_src.find(needle)
        if pos >= 0:
            return pos + len(recv) + 1
    if selector.kind == "call":
        # Anchor text is often the callee chain without `(` (e.g. `foo.bar` not `foo.bar(`).
        dotted = list(
            re.finditer(r"\." + esc + r"(?:\s*[\(<]|\s*$)", expr_src)
        )
        if dotted:
            return dotted[0].start() + 1
        m = re.search(
            _symbol_identifier_pattern(name) + r"(?:\s*[\(<]|\s*$)", expr_src
        )
        if m:
            return m.start()
    elif selector.kind == "attr":
        dotted = list(re.finditer(r"\." + esc + r"\b", expr_src))
        if dotted:
            return dotted[0].start() + 1
    idx = expr_src.find(name)
    return idx if idx >= 0 else 0


def _clamp_position_to_source(text: str, line0: int, col0: int) -> Tuple[int, int]:
    """Keep (line, col) within file bounds so tsserver does not assert on bad offsets."""
    lines_list = text.splitlines()
    if not lines_list:
        return 0, 0
    line0 = max(0, min(int(line0), len(lines_list) - 1))
    line_len = len(lines_list[line0])
    col0 = max(0, min(int(col0), line_len))
    return line0, col0


# ----------------------------
# AST-based callee finding (optional; matches Python robustness)
# ----------------------------

def _strip_outer_parens(s: str) -> str:
    s = s.strip()
    while len(s) >= 2 and s[0] == "(" and s[-1] == ")":
        depth = 0
        ok = True
        for i, ch in enumerate(s):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and i != len(s) - 1:
                    ok = False
                    break
        if ok:
            s = s[1:-1].strip()
        else:
            break
    return s


def _normalize_anchor_for_exact_match(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", "", s)
    s = re.sub(r",\)", ")", s)
    s = re.sub(r",\]", "]", s)
    s = re.sub(r",\}", "}", s)
    s = _strip_outer_parens(s)
    return s


@dataclass
class TsCalleeMatch:
    """One AST-derived candidate for the callee (line0, col0 are 0-based)."""
    line0: int
    col0: int
    expr_src: str
    node_line0: int = 0


def _get_ts_parser(script_path: Path):
    """Return tree-sitter parser for TypeScript or JavaScript, or None if not available."""
    if not _TREE_SITTER_AVAILABLE:
        return None
    ext = script_path.suffix.lower()
    if ext == ".tsx":
        return get_parser("tsx")
    if ext in (".ts", ".mts", ".cts"):
        return get_parser("typescript")
    if ext in (".js", ".jsx", ".mjs", ".cjs"):
        return get_parser("javascript")
    return None


def _node_text(source_bytes: bytes, node) -> str:
    """Extract source segment for a tree-sitter node (byte offsets)."""
    if node is None or node.start_byte is None or node.end_byte is None:
        return ""
    return source_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace")


def _point_contained_in_node(row: int, col: int, node) -> bool:
    """True if (row, col) is inside node's range. Tree-sitter end_point is exclusive."""
    if node is None:
        return False
    sr, sc = node.start_point
    er, ec = node.end_point
    if (row, col) < (sr, sc):
        return False
    if (row, col) >= (er, ec):
        return False
    return True


def _find_node_at_point(node, row: int, col: int):
    """Return the smallest tree-sitter node that contains (row, col), or None."""
    if node is None or not _point_contained_in_node(row, col, node):
        return None
    for i in range(node.child_count):
        child = node.child(i)
        if _point_contained_in_node(row, col, child):
            return _find_node_at_point(child, row, col)
    return node


def _ancestors_include_type(root, target_node, node_types: Tuple[str, ...]) -> bool:
    """True if target_node is equal to or nested inside a node with one of node_types (e.g. call_expression)."""
    if root is None or target_node is None:
        return False
    if root.start_byte == target_node.start_byte and root.end_byte == target_node.end_byte:
        return root.type in node_types
    for i in range(root.child_count):
        child = root.child(i)
        if child.start_byte <= target_node.start_byte and child.end_byte >= target_node.end_byte:
            if child.type in node_types:
                return True
            return _ancestors_include_type(child, target_node, node_types)
    return False


def _definition_location_is_call_site_ast(path: Path, loc: Location) -> bool:
    """
    True if at (loc.start_line, loc.start_char) the code is inside a call_expression or
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

    # LSP and tree-sitter both use character-based columns in their (row, col)
    # points, so we can pass loc.start_char directly.
    row, col = loc.start_line, loc.start_char
    node_at = _find_node_at_point(tree.root_node, row, col)
    if node_at is None:
        return False
    # Walk from root to see if node_at is inside a call_expression or new_expression
    return _ancestors_include_type(
        tree.root_node, node_at, ("call_expression", "new_expression")
    )


def _point_in_range(row: int, col: int, tested_rng: Optional[Tuple[int, int, int, int]]) -> bool:
    if tested_rng is None:
        return True
    start_line, start_col, end_line, end_col = tested_rng
    if row < start_line or row > end_line:
        return False
    if row == start_line and col < start_col:
        return False
    if row == end_line and col > end_col:
        return False
    return True


def _walk_ts_find_callees(
    node,
    source_bytes: bytes,
    tested_rng: Optional[Tuple[int, int, int, int]],
    selector: SnippetSelector,
    out: List[TsCalleeMatch],
) -> None:
    """Recursively find call_expression and member_expression nodes matching selector."""
    if node is None:
        return
    row, col = node.start_point
    if not _point_in_range(row, col, tested_rng):
        return

    if selector.kind == "call" and node.type == "call_expression":
        func = node.child_by_field_name("function")
        if func is None:
            return
        name_node = None
        recv_src: Optional[str] = None
        if func.type == "identifier":
            name = _node_text(source_bytes, func)
            if name == selector.name and selector.receiver is None:
                name_node = func
        elif func.type == "member_expression":
            prop = func.child_by_field_name("property")
            if prop is not None:
                name = _node_text(source_bytes, prop)
                if name == selector.name:
                    obj = func.child_by_field_name("object")
                    recv_src = _node_text(source_bytes, obj).strip() if obj else None
                    if selector.receiver is None or (recv_src and _normalize_anchor_for_exact_match(recv_src) == _normalize_anchor_for_exact_match(selector.receiver or "")):
                        name_node = prop
        if name_node is not None:
            r, c = name_node.start_point
            expr_src = _node_text(source_bytes, node)
            out.append(TsCalleeMatch(line0=r, col0=c, expr_src=expr_src, node_line0=node.start_point[0]))

    if selector.kind == "attr" and node.type == "member_expression":
        prop = node.child_by_field_name("property")
        if prop is not None:
            name = _node_text(source_bytes, prop)
            if name == selector.name:
                obj = node.child_by_field_name("object")
                recv_src = _node_text(source_bytes, obj).strip() if obj else None
                if selector.receiver is None or (recv_src and _normalize_anchor_for_exact_match(recv_src) == _normalize_anchor_for_exact_match(selector.receiver or "")):
                    r, c = prop.start_point
                    expr_src = _node_text(source_bytes, node)
                    out.append(TsCalleeMatch(line0=r, col0=c, expr_src=expr_src, node_line0=node.start_point[0]))

    for i in range(node.child_count):
        _walk_ts_find_callees(node.child(i), source_bytes, tested_rng, selector, out)


def _find_ts_callee_nodes_ast(
    source: str,
    tested_rng: Optional[Tuple[int, int, int, int]],
    selector: SnippetSelector,
    script_path: Path,
) -> List[TsCalleeMatch]:
    """Find callee nodes via tree-sitter AST (only real call/member nodes). Returns [] if parser unavailable or parse fails."""
    parser = _get_ts_parser(script_path)
    if parser is None:
        return []
    try:
        source_bytes = source.encode("utf-8")
        tree = parser.parse(source_bytes)
    except Exception:
        return []
    if tree.root_node is None or tree.root_node.has_error:
        return []
    out: List[TsCalleeMatch] = []
    _walk_ts_find_callees(tree.root_node, source_bytes, tested_rng, selector, out)
    return out


def _extract_tested_function_range_ts_ast(
    source: str,
    function_name: str,
    script_path: Path,
) -> Optional[Tuple[int, int, int, int]]:
    """
    Best-effort (line, col) range for a named function/method body from tree-sitter.
    Used to scope anchor search before the LSP client exists.
    """
    parser = _get_ts_parser(script_path)
    if parser is None:
        return None
    try:
        source_bytes = source.encode("utf-8")
        tree = parser.parse(source_bytes)
    except Exception:
        return None
    if tree.root_node is None or tree.root_node.has_error:
        return None

    def walk(node) -> Optional[Tuple[int, int, int, int]]:
        if node.type in ("function_declaration", "method_definition", "generator_function"):
            name_node = node.child_by_field_name("name")
            if name_node is not None and _node_text(source_bytes, name_node) == function_name:
                sl, sc = node.start_point
                el, ec = node.end_point
                return (int(sl), int(sc), int(el), int(ec))
        for i in range(node.child_count):
            found = walk(node.child(i))
            if found is not None:
                return found
        return None

    return walk(tree.root_node)


def _filter_by_anchor_strict_ts(
    script_lines: List[str],
    candidates: List[TsCalleeMatch],
    anchor: str,
    window: int,
) -> List[TsCalleeMatch]:
    """Mirror Python filter_by_anchor_strict: exact match, then contained, then block contains."""
    anchor_n = _normalize_anchor_for_exact_match(anchor)
    exact: List[TsCalleeMatch] = []
    for m in candidates:
        expr_n = _normalize_anchor_for_exact_match(m.expr_src)
        if anchor_n == expr_n:
            exact.append(m)
    if exact:
        return exact
    contained: List[TsCalleeMatch] = []
    for m in candidates:
        expr_n = _normalize_anchor_for_exact_match(m.expr_src)
        if anchor_n and anchor_n in expr_n:
            contained.append(m)
    if contained:
        return contained
    a2 = re.sub(r"\s+", "", anchor)
    kept: List[TsCalleeMatch] = []
    for m in candidates:
        lo = max(0, m.node_line0 - window)
        hi = min(len(script_lines), m.node_line0 + window + 1)
        block = "\n".join(script_lines[lo:hi])
        if a2 in re.sub(r"\s+", "", block):
            kept.append(m)
    return kept


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

    # DocumentSymbol form: recursive hierarchy
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

    # SymbolInformation form: flat list
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
        # DocumentSymbol tree
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
        # SymbolInformation list
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
        key = (loc.uri, loc.start_line, loc.start_char, loc.end_line, loc.end_char)
        if key in seen:
            continue
        seen.add(key)
        out.append(loc)
    return out


def _char_index_from_line_col(text: str, line0: int, col0: int) -> int:
    """0-based (line, col) -> character index in text (newline-aware)."""
    i = 0
    ln = 0
    n = len(text)
    while ln < line0 and i < n:
        j = text.find("\n", i)
        if j < 0:
            return n
        i = j + 1
        ln += 1
    return i + col0


def _line_col_from_char_index(text: str, index: int) -> Tuple[int, int]:
    """Character index in text -> 0-based (line0, col0)."""
    index = max(0, min(index, len(text)))
    prefix = text[:index]
    line0 = prefix.count("\n")
    last_nl = prefix.rfind("\n")
    col0 = index - (last_nl + 1) if last_nl >= 0 else index
    return line0, col0


def _raw_index_to_flat_index(text: str, raw_i: int) -> int:
    """Map index in raw text (with possible \\r\\n) to index in text.replace('\\r\\n', '\\n')."""
    fi = 0
    ri = 0
    n = len(text)
    target = max(0, min(raw_i, n))
    while ri < target:
        if ri + 1 < n and text[ri] == "\r" and text[ri + 1] == "\n":
            ri += 2
            fi += 1
        else:
            ri += 1
            fi += 1
    return fi


def _flat_index_to_raw_index(text: str, flat_i: int) -> int:
    """Inverse of _raw_index_to_flat_index for valid indices."""
    fi = 0
    ri = 0
    n = len(text)
    while fi < flat_i and ri < n:
        if ri + 1 < n and text[ri] == "\r" and text[ri + 1] == "\n":
            ri += 2
            fi += 1
        else:
            ri += 1
            fi += 1
    return ri


def _find_anchor_candidates_in_range(
    source: str,
    anchor: str,
    *,
    tested_rng: Optional[Tuple[int, int, int, int]],
) -> List[Tuple[int, int, str]]:

    if not anchor:
        return []

    lines = source.splitlines()
    if tested_rng is not None:
        start_line, _, end_line, _ = tested_rng
        lo = max(0, start_line)
        hi = min(len(lines) - 1, end_line)
    else:
        lo, hi = 0, len(lines) - 1

    # Multiline anchors cannot match via single-line find(); search in a char slice.
    if "\n" in anchor or "\r" in anchor:
        start_i = _char_index_from_line_col(source, lo, 0)
        if hi + 1 < len(lines):
            end_i = _char_index_from_line_col(source, hi + 1, 0)
        else:
            end_i = len(source)
        out_m: List[Tuple[int, int, str]] = []
        pos = source.find(anchor, start_i, end_i)
        while pos >= 0:
            line0, col0 = _line_col_from_char_index(source, pos)
            line_text = lines[line0] if 0 <= line0 < len(lines) else ""
            out_m.append((line0, col0, line_text))
            pos = source.find(anchor, pos + 1, end_i)
        if out_m or "\r\n" not in source:
            return out_m
        flat = source.replace("\r\n", "\n")
        s_f = _raw_index_to_flat_index(source, start_i)
        e_f = _raw_index_to_flat_index(source, min(end_i, len(source)))
        pos_f = flat.find(anchor, s_f, e_f)
        while pos_f >= 0:
            raw = _flat_index_to_raw_index(source, pos_f)
            line0, col0 = _line_col_from_char_index(source, raw)
            line_text = lines[line0] if 0 <= line0 < len(lines) else ""
            out_m.append((line0, col0, line_text))
            pos_f = flat.find(anchor, pos_f + 1, e_f)
        return out_m

    out: List[Tuple[int, int, str]] = []
    for line0 in range(lo, hi + 1):
        line = lines[line0]
        if _is_comment_line(line):
            continue
        start = 0
        while True:
            idx = line.find(anchor, start)
            if idx < 0:
                break
            out.append((line0, idx, line))
            start = idx + 1
    return out


def _find_anchor_candidates_by_core(
    source: str,
    selector: SnippetSelector,
    *,
    tested_rng: Optional[Tuple[int, int, int, int]],
) -> List[Tuple[int, int, str]]:
    """
    Fallback: find lines containing the symbol name (e.g. getHighestNode( or .getNodeParameter()
    so we can resolve when the full anchor string doesn't match (formatting / multi-line).
    """
    name = selector.name
    if not name:
        return []
    lines = source.splitlines()
    if tested_rng is not None:
        start_line, _, end_line, _ = tested_rng
        lo = max(0, start_line)
        hi = min(len(lines) - 1, end_line)
    else:
        lo, hi = 0, len(lines) - 1

    out: List[Tuple[int, int, str]] = []
    if selector.kind == "call":
        # Prefer ".name(" or "name(" to avoid matching inside other identifiers
        pattern = name + "("
        alt_pattern = "." + name + "("
    else:
        pattern = name
        alt_pattern = "." + name

    for line0 in range(lo, hi + 1):
        line = lines[line0]
        if _is_comment_line(line):
            continue
        idx = line.find(alt_pattern)
        if idx >= 0:
            col0 = idx + 1  # column of name after "."
        else:
            idx = line.find(pattern)
            col0 = idx
        if idx >= 0:
            out.append((line0, col0, line))
    return out


def _pick_anchor_candidates_with_fallbacks(
    text: str,
    anchor_text: str,
    selector: SnippetSelector,
    tested_rng: Optional[Tuple[int, int, int, int]],
) -> List[Tuple[int, int, str, bool]]:
    """
    Try exact anchor in range, then whole file, then core-pattern (name or .name() in range),
    then core-pattern in whole file. Returns list of (line0, col0, line_text, from_core).
    When multiple from core pattern, prefer single candidate inside tested_rng.
    """
    exact = _find_anchor_candidates_in_range(text, anchor_text, tested_rng=tested_rng)
    if exact:
        return [(line0, col0, lt, False) for line0, col0, lt in exact]
    exact = _find_anchor_candidates_in_range(text, anchor_text, tested_rng=None)
    if exact:
        return [(line0, col0, lt, False) for line0, col0, lt in exact]
    candidates = _find_anchor_candidates_by_core(text, selector, tested_rng=tested_rng)
    if candidates:
        if tested_rng is not None and len(candidates) > 1:
            start_line, _, end_line, _ = tested_rng
            in_range = [(line0, col0, lt) for line0, col0, lt in candidates if start_line <= line0 <= end_line]
            if in_range:
                return [(in_range[0][0], in_range[0][1], in_range[0][2], True)]
        one = candidates[0]
        return [(one[0], one[1], one[2], True)]
    candidates = _find_anchor_candidates_by_core(text, selector, tested_rng=None)
    if candidates:
        if tested_rng is not None and len(candidates) > 1:
            start_line, _, end_line, _ = tested_rng
            in_range = [(line0, col0, lt) for line0, col0, lt in candidates if start_line <= line0 <= end_line]
            if in_range:
                return [(in_range[0][0], in_range[0][1], in_range[0][2], True)]
        one = candidates[0]
        return [(one[0], one[1], one[2], True)]
    return []


@dataclass(frozen=True)
class DefCandidate:
    loc: Location
    path: Path
    is_d_ts: bool
    is_repo_local: bool
    in_node_modules: bool
    path_len: int


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
        is_repo_local=is_repo_local,
        in_node_modules=in_node_modules,
        path_len=len(str(p)),
    )


def _get_or_create_ts_lsp_client(
    repo_root: Path,
    script_path: Path,
    lang_id: str,
    cmd: List[str],
    root_uri: str,
    workspace_uris: List[str],
) -> GenericLSPClient:
    cache_key = _ts_lsp_client_cache_key(repo_root, script_path, lang_id)
    cached = _TS_LSP_CLIENTS.get(cache_key)
    if cached is None:
        primary = workspace_uris[0] if workspace_uris else root_uri
        cached = GenericLSPClient(
            server_cmd=cmd,
            root_uri=primary,
            language_id=lang_id,
            init_options={},
            workspace_folder_uris=workspace_uris or None,
        )
        _TS_LSP_CLIENTS[cache_key] = cached
    return cached


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
            "start": {"line0": loc.start_line, "col0": loc.start_char},
            "end": {"line0": loc.end_line, "col0": loc.end_char},
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
                        "col0": export_surface_loc.start_char,
                    },
                    "end": {
                        "line0": export_surface_loc.end_line,
                        "col0": export_surface_loc.end_char,
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
        # Prisma-style generated client top-of-file window.
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
                "col0": chosen_def.loc.start_char,
            },
            "end": {
                "line0": chosen_def.loc.end_line,
                "col0": chosen_def.loc.end_char,
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
            outer["callee_documentation"] = client.hover(loc.uri, loc.start_line, loc.start_char)
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


def _try_resolve_primary_go_to_source_definition(
    *,
    result: Dict[str, Any],
    repo_root: Path,
    script_path: Path,
    text: str,
    doc_uri: str,
    line0: int,
    col0: int,
    selector: SnippetSelector,
    lang_id: str,
    cmd: List[str],
    root_uri: str,
    workspace_uris: List[str],
    use_go_to_source_definition: bool,
    client: Optional[GenericLSPClient],
) -> Tuple[Optional[Dict[str, Any]], Optional[GenericLSPClient]]:
    """
    Primary resolution: TypeScript LSP ``_typescript.goToSourceDefinition`` at the call site.
    Returns a finished ``result`` dict when this yields a usable definition; otherwise
    ``(None, client)`` so callers can fall back to other LSP methods.
    """
    if not use_go_to_source_definition:
        return None, client

    try:
        if client is None:
            client = _get_or_create_ts_lsp_client(
                repo_root, script_path, lang_id, cmd, root_uri, workspace_uris
            )
        client.open_document(doc_uri, text)
        time.sleep(0.15)
        source_def_locs = client.goto_source_definition(doc_uri, line0, col0)
    except Exception:
        return None, client

    if not source_def_locs:
        return None, client

    locs_json = [loc.to_json() for loc in source_def_locs]
    result["source_definition_locations"] = locs_json
    result["definitions_all"] = locs_json
    result["definitions_all_filtered"] = locs_json

    symbol_name_for_choice = selector.name if selector.name else None
    receiver_parent_hint: Optional[str] = None
    if selector.receiver:
        receiver_parent_hint = selector.receiver.split(".")[-1].strip() or None
    prefer_same_doc_uri = (
        doc_uri
        if selector.kind == "attr" and selector.receiver == "this"
        else None
    )

    chosen_def, debug = _choose_one_definition(
        repo_root,
        source_def_locs,
        symbol_name=symbol_name_for_choice,
        usage_kind=selector.kind,
        prefer_same_document_uri=prefer_same_doc_uri,
        preferred_locations=source_def_locs,
    )
    if chosen_def is None:
        return None, client

    full_def_source = _read_definition_source(chosen_def.loc, symbol_name_for_choice)
    full_def_source = _prefer_lib_global_constructor_snippet(
        full_def_source,
        chosen_def.path,
        symbol_name_for_choice,
        usage_kind=selector.kind,
    )

    upgraded_from_declaration, declaration_surface_snapshot, runtime_implementation, ext_trace = (
        _try_external_declaration_runtime_upgrade(
            client,
            repo_root,
            chosen_def,
            full_def_source,
            symbol_name_for_choice,
        )
    )
    if upgraded_from_declaration and ext_trace is not None:
        debug = {
            **debug,
            "external_runtime_resolution": ext_trace,
        }
    elif chosen_def.is_d_ts and chosen_def.in_node_modules:
        return None, client

    if (
        symbol_name_for_choice
        and not _definition_source_matches_symbol(full_def_source, symbol_name_for_choice)
    ):
        try:
            syms = client.document_symbols(chosen_def.loc.uri)
            sym_loc = _find_symbol_location_from_document_symbols(
                syms,
                uri=chosen_def.loc.uri,
                symbol_name=symbol_name_for_choice,
                hint_line0=chosen_def.loc.start_line,
                parent_name_hint=receiver_parent_hint,
            )
            if sym_loc is not None:
                refined = _build_def_candidate(repo_root, sym_loc)
                refined_src = _read_definition_source(refined.loc, symbol_name_for_choice)
                if _definition_source_matches_symbol(refined_src, symbol_name_for_choice):
                    chosen_def = refined
                    full_def_source = refined_src
                    debug = {**debug, "note": "primary_refined_via_document_symbols"}
        except Exception:
            pass
        if not _definition_source_matches_symbol(full_def_source, symbol_name_for_choice):
            return None, client

    outer = _build_outer_definition(
        chosen_def=chosen_def,
        repo_root=repo_root,
        full_def_source=full_def_source,
        client=client,
        declaration_surface=declaration_surface_snapshot if upgraded_from_declaration else None,
        runtime_implementation=runtime_implementation,
    )

    result["chosen_definition_reason"] = {
        **debug,
        "note": "go_to_source_definition_primary",
        "go_to_source_definition": True,
    }
    result["definitions"] = [
        {
            "outer_ok": True,
            "outer_error": None,
            "outer_definition": outer,
            "argument_usages_resolved": [],
        }
    ]
    result["ok"] = True
    return result, client


def _definition_source_is_import_or_export(loc: Location, symbol_name: Optional[str]) -> bool:
    """True for import lines and export re-exports, not for real exported declarations."""
    src = _read_definition_source(loc, symbol_name)
    if not src:
        return False
    stripped = src.strip()
    if stripped.startswith("import "):
        return True
    if not stripped.startswith("export "):
        return False
    # Keep real exported declarations (class/function/const/etc.).
    if re.match(r"^export\s+(?:default\s+)?(?:abstract\s+)?(?:class|interface|type|enum|function|const|let|var)\b", stripped):
        return False
    # Treat export-only forms as re-export sites.
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
    # Usage pattern: symbolName() followed by .should( or similar (Chai, Jest, etc.)
    if re.search(r"\.should\s*\(", s) or re.search(r"\.expect\s*\(", s):
        return True
    # Single line that is just symbolName(...) with no declaration keywords (narrow heuristic)
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
    # Find import that mentions symbol_name: import { x, symbol_name, y } from 'path' or import symbol_name from 'path'
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
            continue  # node_modules; skip
        if not resolved.exists():
            # TypeScript/JS often omit extension in imports; try .ts, .tsx, .js, .jsx
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
            continue  # outside repo
        try:
            export_text = resolved.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        lines = export_text.splitlines()
        # Find export const symbol_name = or export function symbol_name
        export_re = re.compile(
            r"export\s+(?:const|function|async\s+function)\s+" + re.escape(symbol_name) + r"\b"
        )
        for i, line in enumerate(lines):
            if export_re.search(line):
                return (resolved, i)
    return None


def _location_has_implementation_body(loc: Location, symbol_name: Optional[str]) -> bool:
    """True if the source at this location looks like a method/function body (has `{`), not just a declaration."""
    src = _read_definition_source(loc, symbol_name)
    if not src or "{" not in src:
        return False
    # Exclude any import/export: "import { x } from ..." and "export { x }" contain "{" but are
    # not implementations. So we always prefer the real definition over an import/reexport site.
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
            (loc.uri, loc.start_line, loc.start_char, loc.end_line, loc.end_char)
            for loc in preferred_locations
        }
        preferred_cands = [
            c
            for c in candidates
            if (c.loc.uri, c.loc.start_line, c.loc.start_char, c.loc.end_line, c.loc.end_char)
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

    # For `this.foo`, LSP often returns both the inject/property site (this file) and
    # typeDefinition (e.g. nested field on the service class). Shorter-path tie-break
    # must not override the usage file when a candidate exists there.
    if prefer_same_document_uri and usage_kind == "attr":
        same_doc = [c for c in pool if c.loc.uri == prefer_same_document_uri]
        if same_doc:
            pool = same_doc
            debug["note"] = f"{debug['note']}; prefer_usage_document_uri"

    # Drop import/export sites when we have any non-import/export candidate (e.g. successToast:
    # prefer cypress/pages/notifications.ts over cypress/composables/folders.ts import).
    if symbol_name:
        non_import_export = [c for c in pool if not _definition_source_is_import_or_export(c.loc, symbol_name)]
        if non_import_export:
            pool = non_import_export
            debug["note"] = f"dropped_import_export_sites_kept={len(pool)}"
    elif len(pool) > 1:
        declaration_like = [c for c in pool if _definition_source_looks_like_declaration_site(c.loc)]
        if declaration_like:
            pool = declaration_like
            debug["note"] = f"preferred_declaration_like_sites_kept={len(pool)}"

    # Prefer implementation (has method/function body) over interface/declaration when we have both
    if symbol_name and usage_kind == "call" and len(pool) > 1:
        with_body = [c for c in pool if _location_has_implementation_body(c.loc, symbol_name)]
        if with_body:
            pool = with_body
            debug["note"] = f"preferred_implementation_over_declaration_kept={len(pool)}"

    pool_sorted = sorted(
        pool,
        key=lambda c: (c.path_len, c.path.as_posix(), c.loc.start_line, c.loc.start_char),
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


def _match_snippet_for_nested_offsets(
    text: str,
    snippet: str,
    alternatives: List[str],
    hint_index: int,
) -> Optional[Tuple[int, bool]]:
    """
    Locate snippet (or alternative) in file near hint_index.

    Returns (start, in_flat_space). If in_flat_space is False, start is a raw
    character index in text; if True, start indexes text.replace('\\r\\n', '\\n').
    """
    needles: List[str] = []
    for n in [snippet, *alternatives]:
        if n and n not in needles:
            needles.append(n)
    margin = 8000
    for needle in needles:
        if not needle:
            continue
        lo = max(0, hint_index - margin)
        hi = min(len(text), hint_index + margin + len(needle))
        pos = text.find(needle, lo, hi)
        if pos >= 0:
            return (pos, False)
        pos = text.find(needle, max(0, hint_index - 50000), len(text))
        if pos >= 0:
            return (pos, False)
    if "\r\n" not in text:
        return None
    flat = text.replace("\r\n", "\n")
    hint_f = _raw_index_to_flat_index(text, min(hint_index, len(text)))
    for needle in needles:
        if not needle:
            continue
        lo = max(0, hint_f - margin)
        hi = min(len(flat), hint_f + margin + len(needle))
        pf = flat.find(needle, lo, hi)
        if pf < 0:
            pf = flat.find(needle, max(0, hint_f - 50000), len(flat))
        if pf >= 0:
            return (pf, True)
    return None


def _nested_usage_to_file_line_col(
    text: str,
    snippet: str,
    outer_line0: int,
    outer_anchor_col0: int,
    offset_in_snippet: int,
    expr_src_alt: str,
) -> Tuple[int, int]:
    """
    Map offset within the callee snippet string to (line0, col0) in the file.
    Single-line snippets keep anchor_col0 + offset (legacy). Multi-line snippets
    use snippet-relative indices in the file text.
    """
    if "\n" not in snippet and "\r" not in snippet:
        return outer_line0, outer_anchor_col0 + offset_in_snippet
    hint = _char_index_from_line_col(text, outer_line0, outer_anchor_col0)
    alts = [expr_src_alt] if expr_src_alt != snippet else []
    match = _match_snippet_for_nested_offsets(text, snippet, alts, hint)
    if match is None:
        return outer_line0, outer_anchor_col0 + offset_in_snippet
    start, in_flat = match
    if in_flat:
        flat = text.replace("\r\n", "\n")
        tf = start + offset_in_snippet
        if tf < 0 or tf > len(flat):
            return outer_line0, outer_anchor_col0 + offset_in_snippet
        target = _flat_index_to_raw_index(text, tf)
    else:
        target = start + offset_in_snippet
        if target < 0 or target > len(text):
            return outer_line0, outer_anchor_col0 + offset_in_snippet
    return _line_col_from_char_index(text, target)


def _nested_usages_in_snippet(snippet: str, outer_name: str) -> List[Dict[str, Any]]:

    out: List[Dict[str, Any]] = []

    # Attribute patterns: obj.prop
    attr_re = re.compile(r"([A-Za-z_$][A-Za-z0-9_$]*)\s*\.\s*([A-Za-z_$][A-Za-z0-9_$]*)")
    for m in attr_re.finditer(snippet):
        recv, nm = m.group(1), m.group(2)
        # Skip outer name if it happens to be part of something like "outer.inner"
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

    # Call patterns: name(...)
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



def resolve_from_snippet(
    *,
    repo_root: Path,
    script_path: Path,
    tested_function: str,
    snippet: str,
    anchor: Optional[str] = None,
    window: int = 3,
    server_cmd: Optional[List[str]] = None,
    use_go_to_source_definition: bool = True,
) -> Dict[str, Any]:
    #---phase 1: prep, find the file and clean the callee anchor, get uri for config files---#
    prepared = prepare_resolution(
        repo_root=repo_root,
        script_path=script_path,
        tested_function=tested_function,
        snippet=snippet,
        anchor=anchor,
        window=window,
        server_cmd=server_cmd,
        use_go_to_source_definition=use_go_to_source_definition,
    )
    result = prepared.result
    if not prepared.ok or prepared.context is None:
        return result

    ctx = prepared.context
    repo_root = ctx.repo_root
    script_path = ctx.file_path
    text = ctx.text
    selector = ctx.selector
    anchor_text = ctx.search_text
    usage_hint = anchor_text
    cmd = ctx.cmd
    root_uri = ctx.root_uri
    lang_id = ctx.lang_id
    doc_uri = ctx.doc_uri
    workspace_uris = ctx.workspace_uris

    #---phase 2 start: find location of the callee in the file using ast---#
    client: Optional[GenericLSPClient] = None

    script_lines = text.splitlines()
    tested_rng: Optional[Tuple[int, int, int, int]] = None
    if tested_function:
        tested_rng = _extract_tested_function_range_ts_ast(text, tested_function, script_path)

    chosen_match = None
    use_ast = _TREE_SITTER_AVAILABLE

    if use_ast:
        usage_candidates = _find_ts_callee_nodes_ast(text, tested_rng, selector, script_path)
        if usage_candidates:
            anchored = _filter_by_anchor_strict_ts(script_lines, usage_candidates, anchor_text, window)
            if anchored:
                # When anchor is not unique, take the first match
                m = anchored[0]
                pretty = (
                    f"{selector.receiver}.{selector.name}"
                    if selector.receiver
                    else selector.name
                )
                chosen_match = {
                    "kind": selector.kind,
                    "pretty": pretty,
                    "expr_src": m.expr_src,
                    "ref": {
                        "path": str(script_path),
                        "line1": m.line0 + 1,
                        "col1": m.col0 + 1,
                        "line0": m.line0,
                        "col0": m.col0,
                    },
                    "line_text": script_lines[m.line0] if 0 <= m.line0 < len(script_lines) else "",
                    "meta": {"pattern": "ast"},
                }
                for c in usage_candidates:
                    result["matches"]["candidates"].append({
                        "kind": selector.kind,
                        "pretty": pretty,
                        "expr_src": c.expr_src,
                        "ref": {"path": str(script_path), "line1": c.line0 + 1, "col1": c.col0 + 1, "line0": c.line0, "col0": c.col0},
                        "line_text": script_lines[c.line0] if 0 <= c.line0 < len(script_lines) else "",
                        "meta": {"pattern": "ast"},
                    })
                result["matches"]["anchored"] = [chosen_match] if chosen_match else []
                result["matches"]["chosen"] = chosen_match

    if chosen_match is None:
        candidates_raw = _pick_anchor_candidates_with_fallbacks(
            text, anchor_text, selector, tested_rng
        )
        if not candidates_raw:
            result["error"] = "No candidates found by anchor inside tested_function (or file if range unknown)."
            return result

        for line0, col0, line_text, from_core in candidates_raw:
            pretty = (
                f"{selector.receiver}.{selector.name}"
                if selector.receiver
                else selector.name
            )
            result["matches"]["candidates"].append(
                {
                    "kind": selector.kind,
                    "pretty": pretty,
                    "expr_src": anchor_text,
                    "ref": {
                        "path": str(script_path),
                        "line1": line0 + 1,
                        "col1": col0 + 1,
                        "line0": line0,
                        "col0": col0,
                    },
                    "line_text": line_text,
                    "meta": {"pattern": "core_fallback" if from_core else "anchor_substring"},
                }
            )
        result["matches"]["anchored"] = list(result["matches"]["candidates"])
        # When anchor is not unique, take the first match
        if result["matches"]["anchored"]:
            chosen_match = result["matches"]["anchored"][0]
            result["matches"]["chosen"] = chosen_match

    if chosen_match is None:
        result["error"] = "No matching callee found for this snippet."
        result["ok"] = False
        return result

    line0 = chosen_match["ref"]["line0"]
    anchor_col0 = chosen_match["ref"]["col0"]
    expr_src = chosen_match.get("expr_src") or anchor_text
    if chosen_match.get("meta", {}).get("pattern") in ("ast", "core_fallback"):
        col0 = anchor_col0
    else:
        rel_idx = _expr_src_offset_for_selector_name(expr_src, selector)
        if "\n" in expr_src or "\r" in expr_src:
            line0, col0 = _nested_usage_to_file_line_col(
                text,
                expr_src,
                line0,
                anchor_col0,
                rel_idx,
                anchor_text,
            )
        else:
            col0 = anchor_col0 + rel_idx if rel_idx >= 0 else anchor_col0

    line0, col0 = _clamp_position_to_source(text, line0, col0)
    result["navigation_position"] = {"line0": line0, "col0": col0}
    
    #---phase 2 ends, the cursor is set to the exact callee position----#
    #---phase 3 starts: try using go to source definition from lsp using set ups from step 1 and 2---#

    outer_item: Dict[str, Any] = {
        "outer_ok": False,
        "outer_error": None,
        "outer_definition": None,
        "argument_usages_resolved": [],
    }

    primary_result, client = _try_resolve_primary_go_to_source_definition(
        result=result,
        repo_root=repo_root,
        script_path=script_path,
        text=text,
        doc_uri=doc_uri,
        line0=line0,
        col0=col0,
        selector=selector,
        lang_id=lang_id,
        cmd=cmd,
        root_uri=root_uri,
        workspace_uris=workspace_uris,
        use_go_to_source_definition=use_go_to_source_definition,
        client=client,
    )
    if primary_result is not None:
        return primary_result

    #---phase 4: LSP go to definition / typeDefinition / implementation if phase 3 didn't work---#

    try:
        if client is None:
            client = _get_or_create_ts_lsp_client(
                repo_root, script_path, lang_id, cmd, root_uri, workspace_uris
            )

            client.open_document(doc_uri, text)
            time.sleep(0.2)

            if tested_rng is None:
                try:
                    symbols = client.document_symbols(doc_uri)
                    sym_rng = _extract_function_range_from_symbols(symbols, tested_function)
                    if sym_rng is not None:
                        tested_rng = sym_rng
                except Exception:
                    pass

        if selector.kind == "attr":
            locs = []
            locs.extend(client.goto_definition(doc_uri, line0, col0))
            locs.extend(client.goto_type_definition(doc_uri, line0, col0))
            locs.extend(client.goto_implementation(doc_uri, line0, col0))
            locs = _dedupe_locations(locs)
        else:
            locs = []
            locs.extend(client.goto_implementation(doc_uri, line0, col0))
            if not locs:
                locs.extend(client.goto_definition(doc_uri, line0, col0))
            # TypeScript often resolves method calls to implementation via typeDefinition
            if not locs:
                locs = client.goto_type_definition(doc_uri, line0, col0)
            locs = _dedupe_locations(locs)
    except Exception as e:
        result["error"] = f"LSP definition request failed: {e}"
        return result

    result["definitions_all"] = [loc.to_json() for loc in locs]
    result["definitions_all_filtered"] = [loc.to_json() for loc in locs]

    if not locs:
        outer_item["outer_error"] = "No definition found from TypeScript LSP."
        result["definitions"] = [outer_item]
        result["error"] = outer_item["outer_error"]
        result["ok"] = False
        return result

    # Use the accessed symbol name for both calls and attributes so candidate
    # validation can reject nearby-but-wrong type/class locations.
    symbol_name_for_choice = selector.name if selector.name else None
    receiver_parent_hint: Optional[str] = None
    if selector.receiver:
        # e.g. this.prisma.personalAccessToken.create -> parent hint personalAccessToken
        receiver_parent_hint = selector.receiver.split(".")[-1].strip() or None
    prefer_same_doc_uri = (
        doc_uri
        if selector.kind == "attr" and selector.receiver == "this"
        else None
    )
    chosen_def, debug = _choose_one_definition(
        repo_root,
        locs,
        symbol_name=symbol_name_for_choice,
        usage_kind=selector.kind,
        prefer_same_document_uri=prefer_same_doc_uri,
    )
    result["chosen_definition_reason"] = debug

    if chosen_def is None:
        outer_item["outer_error"] = "No valid implementation found after filtering."
        result["definitions"] = [outer_item]
        result["error"] = outer_item["outer_error"]
        result["ok"] = False
        return result

    full_def_source = _read_definition_source(
        chosen_def.loc,
        symbol_name_for_choice,
        usage_hint=usage_hint,
    )
    full_def_source = _prefer_lib_global_constructor_snippet(
        full_def_source,
        chosen_def.path,
        symbol_name_for_choice,
        usage_kind=selector.kind,
    )
    #---phase 4: step 2---
    # Second hop when LSP landed on a non-definition site (import/re-export or call usage).
    # can be merged with phase 3
    # module 
    fix_import = bool(
        symbol_name_for_choice
        and _definition_source_is_import_or_export(chosen_def.loc, symbol_name_for_choice)
    )
    fix_call = bool(
        symbol_name_for_choice
        and full_def_source
        and (
            _definition_location_is_call_site_ast(chosen_def.path, chosen_def.loc)
            or _definition_source_looks_like_usage(
                chosen_def.loc,
                symbol_name_for_choice,
                doc_uri,
                full_def_source,
            )
        )
    )

    if fix_import or fix_call:
        if fix_call:
            found = _find_definition_via_imports(script_path, symbol_name_for_choice, repo_root)
            if found:
                def_path_found, def_line0 = found
                loc_found = Location(
                    uri=file_uri(def_path_found),
                    start_line=def_line0,
                    start_char=0,
                    end_line=def_line0,
                    end_char=0,
                )
                chosen_def = _build_def_candidate(repo_root, loc_found)
                full_def_source = _read_definition_source(
                    loc_found, symbol_name_for_choice, usage_hint=usage_hint
                )
                if full_def_source:
                    result["chosen_definition_reason"] = {
                        **result.get("chosen_definition_reason", {}),
                        "note": "definition_via_imports_followed",
                    }
                    fix_call = bool(
                        _definition_location_is_call_site_ast(chosen_def.path, chosen_def.loc)
                        or _definition_source_looks_like_usage(
                            chosen_def.loc,
                            symbol_name_for_choice,
                            doc_uri,
                            full_def_source,
                        )
                    )

        fix_import = bool(
            symbol_name_for_choice
            and _definition_source_is_import_or_export(chosen_def.loc, symbol_name_for_choice)
        )
        if fix_import or fix_call:
            try:
                second_locs = client.goto_definition(
                    chosen_def.loc.uri,
                    chosen_def.loc.start_line,
                    chosen_def.loc.start_char,
                )
                if second_locs:
                    if fix_call:
                        second_candidates_with_def = [
                            loc
                            for loc in second_locs
                            if not _definition_location_is_call_site_ast(
                                uri_to_path(loc.uri), loc
                            )
                            and not _definition_source_looks_like_usage(
                                loc,
                                symbol_name_for_choice,
                                doc_uri,
                                _read_definition_source(
                                    loc,
                                    symbol_name_for_choice,
                                    usage_hint=usage_hint,
                                ),
                            )
                        ]
                        pool = (
                            second_candidates_with_def
                            if second_candidates_with_def
                            else second_locs
                        )
                    else:
                        pool = second_locs
                    second_chosen, _ = _choose_one_definition(
                        repo_root,
                        pool,
                        symbol_name=symbol_name_for_choice,
                        usage_kind=selector.kind,
                        prefer_same_document_uri=prefer_same_doc_uri,
                    )
                    if second_chosen is not None:
                        second_src = _read_definition_source(
                            second_chosen.loc,
                            symbol_name_for_choice,
                            usage_hint=usage_hint,
                        )
                        accept = bool(second_src)
                        if accept and fix_import:
                            accept = not _definition_source_is_import_or_export(
                                second_chosen.loc, symbol_name_for_choice
                            )
                        if accept and fix_call:
                            accept = not _definition_location_is_call_site_ast(
                                second_chosen.path, second_chosen.loc
                            ) and not _definition_source_looks_like_usage(
                                second_chosen.loc,
                                symbol_name_for_choice,
                                doc_uri,
                                second_src or "",
                            )
                        if accept:
                            chosen_def = second_chosen
                            full_def_source = second_src
                            result["chosen_definition_reason"] = {
                                **result.get("chosen_definition_reason", {}),
                                "note": (
                                    "second_hop_from_import_to_definition"
                                    if fix_import and not fix_call
                                    else "second_hop_from_call_site_to_definition"
                                ),
                            }
            except Exception:
                pass

    upgraded_from_declaration, declaration_surface_snapshot, runtime_implementation, ext_trace = (
        _try_external_declaration_runtime_upgrade(
        ## python parse to AST 
            client,
            repo_root,
            chosen_def,
            full_def_source,
            symbol_name_for_choice,
        )
    )
    if ext_trace is not None:
        result["chosen_definition_reason"] = {
            **(result.get("chosen_definition_reason") or {}),
            "external_runtime_resolution": ext_trace,
        }
    #---phase 5: step 2---
    # After external runtime upgrade, verify symbol anchoring again. Some packages (fp-ts,
    # prisma generated clients) can still return broad top-of-file windows from runtime files.
    if (
        client is not None
        and symbol_name_for_choice
        and not _definition_source_matches_symbol(full_def_source, symbol_name_for_choice)
    ):
        try:
            syms = client.document_symbols(chosen_def.loc.uri)
            sym_loc = _find_symbol_location_from_document_symbols(
                syms,
                uri=chosen_def.loc.uri,
                symbol_name=symbol_name_for_choice,
                hint_line0=chosen_def.loc.start_line,
                parent_name_hint=receiver_parent_hint,
            )
            if sym_loc is not None:
                refined = _build_def_candidate(repo_root, sym_loc)
                refined_src = _read_definition_source(
                    refined.loc,
                    symbol_name_for_choice,
                    usage_hint=usage_hint,
                )
                if _definition_source_matches_symbol(refined_src, symbol_name_for_choice):
                    chosen_def = refined
                    full_def_source = refined_src
                    result["chosen_definition_reason"] = {
                        **(result.get("chosen_definition_reason") or {}),
                        "note": "post_upgrade_refined_via_document_symbols",
                    }
        except Exception:
            pass
        # If runtime upgrade still isn't anchored to the symbol, return the original declaration surface.
        if (
            declaration_surface_snapshot is not None
            and not _definition_source_matches_symbol(full_def_source, symbol_name_for_choice)
        ):
            try:
                ds = declaration_surface_snapshot
                ds_range = ds.get("range") or {}
                ds_start = (ds_range.get("start") or {})
                ds_end = (ds_range.get("end") or {})
                decl_loc = Location(
                    uri=str(ds.get("uri") or ""),
                    start_line=int(ds_start.get("line0", 0)),
                    start_char=int(ds_start.get("col0", 0)),
                    end_line=int(ds_end.get("line0", 0)),
                    end_char=int(ds_end.get("col0", 0)),
                )
                decl_cand = _build_def_candidate(repo_root, decl_loc)
                decl_src = _read_definition_source(
                    decl_loc, symbol_name_for_choice, usage_hint=usage_hint
                )
                if _definition_source_matches_symbol(decl_src, symbol_name_for_choice):
                    chosen_def = decl_cand
                    full_def_source = decl_src
                    result["chosen_definition_reason"] = {
                        **(result.get("chosen_definition_reason") or {}),
                        "note": "runtime_unresolved_fell_back_to_declaration",
                    }
            except Exception:
                pass

    outer = _build_outer_definition(
        chosen_def=chosen_def,
        repo_root=repo_root,
        full_def_source=full_def_source,
        client=client,
        declaration_surface=declaration_surface_snapshot if upgraded_from_declaration else None,
        runtime_implementation=runtime_implementation,
    )
    #---phase 6---- check the nested callee
    #--- edit this to be ast separated and resurvie
    
    nested_recs: List[Dict[str, Any]] = []
    for u in _nested_usages_in_snippet(snippet, selector.name):
        try:
            n_line0, n_col0 = _nested_usage_to_file_line_col(
                text,
                snippet,
                line0,
                anchor_col0,
                int(u["offset"]),
                expr_src,
            )
            u_locs = client.goto_definition(doc_uri, n_line0, n_col0)

            prefer_nested_doc = (
                doc_uri
                if u.get("kind") == "attr" and u.get("receiver") == "this"
                else None
            )
            chosen_u, debug_u = _choose_one_definition(
                repo_root,
                u_locs,
                symbol_name=u["name"] if u.get("kind") == "call" else None,
                usage_kind=u.get("kind"),
                prefer_same_document_uri=prefer_nested_doc,
            )
            rec: Dict[str, Any] = {
                "usage": {
                    "kind": u["kind"],
                    "name": u["name"],
                    "receiver": u["receiver"],
                    "line0": n_line0,
                    "col0": n_col0,
                    "node_line0": n_line0,
                    "pattern": u["pattern"],
                },
                "definitions_all": [L.to_json() for L in u_locs],
                "chosen_definition_reason": debug_u,
                "definition": None,
                "ok": False,
                "error": None,
            }

            if not u_locs:
                rec["error"] = "no_definitions_from_lsp"
            elif chosen_u is None:
                rec["error"] = "no_valid_implementation_after_filtering"
            else:
                uloc = chosen_u.loc
                upath = chosen_u.path
                ddef: Dict[str, Any] = {**uloc.to_json()}
                ddef["path"] = upath.as_posix()
                ddef["directory"] = upath.parent.as_posix()
                try:
                    urel = upath.resolve().relative_to(repo_root.resolve())
                    ddef["repo_relative_path"] = urel.as_posix()
                    ddef["repo_relative_dir"] = urel.parent.as_posix()
                except Exception:
                    pass
                full_src = _read_definition_source(
                    uloc,
                    u["name"] if u.get("kind") == "call" else None,
                )
                # For single-line property/field declarations (e.g. "x: TypeName;"),
                # resolve the referenced type and use its full source.
                if (
                    u.get("kind") == "attr"
                    and full_src
                    and "\n" not in full_src
                    and full_src.strip().endswith(";")
                ):
                    try:
                        def_lines = upath.read_text(encoding="utf-8", errors="replace").splitlines()
                        if 0 <= uloc.start_line < len(def_lines):
                            line = def_lines[uloc.start_line]
                            type_info = _get_referenced_type_on_line(line)
                            if type_info:
                                type_name, type_col = type_info
                                type_locs = client.goto_definition(uloc.uri, uloc.start_line, type_col)
                                if not type_locs:
                                    type_locs = client.goto_type_definition(uloc.uri, uloc.start_line, type_col)
                                if type_locs:
                                    type_loc = type_locs[0]
                                    type_src = _read_definition_source(type_loc, type_name)
                                    if type_src:
                                        full_src = type_src
                                    elif type_loc.uri != uloc.uri or type_loc.start_line != uloc.start_line:
                                        type_src = _read_definition_source(type_loc, None)
                                        if type_src:
                                            full_src = type_src
                    except Exception:
                        pass
                ddef["full_def_source"] = full_src
                try:
                    ddef["callee_documentation"] = client.hover(
                        uloc.uri, uloc.start_line, uloc.start_char
                    )
                except Exception:
                    ddef["callee_documentation"] = None
                rec["definition"] = ddef
                rec["ok"] = True

            nested_recs.append(rec)
        except Exception as e:
            nested_recs.append(
                {
                    "usage": u,
                    "definitions_all": [],
                    "chosen_definition_reason": {"note": "nested_resolution_failed"},
                    "definition": None,
                    "ok": False,
                    "error": f"{type(e).__name__}: {e}",
                }
            )

    outer_item["outer_ok"] = True
    outer_item["outer_definition"] = outer
    outer_item["argument_usages_resolved"] = nested_recs
    result["definitions"] = [outer_item]
    result["ok"] = True
    return result

if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--script-path", required=True)
    ap.add_argument("--tested-function", required=True)
    ap.add_argument("--callee", required=True)
    ap.add_argument(
        "--no-go-to-source-definition",
        action="store_true",
        help="Disable TypeScript 4.7+ Go to Source Definition (compare with legacy behavior)",
    )
    args = ap.parse_args()

    res = resolve_from_snippet(
        repo_root=Path(args.repo_root),
        script_path=Path(args.script_path),
        tested_function=args.tested_function,
        snippet=args.callee,
        anchor=args.callee,
        use_go_to_source_definition=not args.no_go_to_source_definition,
    )
    print(json.dumps(res, indent=2, ensure_ascii=False))
