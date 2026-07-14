from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from lsp_client import Location, uri_to_path
from ts_ast import get_ts_parser as _get_ts_parser, node_text as _node_text
from ts_definition_ops import (  # noqa: F401 — re-exported for callers/tests
    DefCandidate,
    _build_def_candidate,
    _choose_one_definition,
    _dedupe_locations,
    _definition_location_is_call_site_ast,
    _extract_function_range_from_symbols,
    _find_constructor_snippet,
    _prefer_lib_global_constructor_snippet,
)
from ts_go_to_source_definition import try_go_to_source_definition
from ts_locate_callee import locate_callee
from ts_prepare_resolution import (  # noqa: F401 — re-exported public helpers
    nearest_tsconfig_dir,
    prepare_resolution,
    ts_server_cmd as _ts_server_cmd,
    ts_workspace_folder_uris,
)
from ts_resolve_lsp_definition import resolve_via_lsp_definition
from ts_text_coords import is_comment_line as _is_comment_line


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

    #---phase 2: find location of the callee in the file using ast#
    located = locate_callee(ctx, result)
    result = located.result
    if not located.ok:
        return result

    ctx = located.context

    #---phase 3: try goToSourceDefinition using setups from phases 1 and 2---#
    source = try_go_to_source_definition(ctx, result)
    result = source.result
    ctx = source.context
    if source.resolved:
        return result

    #---phase 4: LSP definition / typeDefinition / implementation (+ nested usages)---#
    return resolve_via_lsp_definition(ctx, result).result


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
