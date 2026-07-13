"""Locate a TypeScript/JavaScript callee in the usage file (phase 2).

Given a prepared ResolutionContext, find the usage site (AST first, text
fallback second), compute the navigation cursor, and write:

  - ctx.expr_rng / ctx.callee_location
  - result["matches"] / result["navigation_position"]

Does not talk to the LSP. Depends on models + shared ts_ast / ts_text_coords only
(not on code_navigation_TypeScript).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from models import (
    CalleeLocation,
    Position,
    ResolutionContext,
    SnippetSelector,
    TestedRange,
    apply_callee_to_result,
    build_failure_result,
    build_match_entry,
)
from ts_ast import TREE_SITTER_AVAILABLE, get_ts_parser, node_text, point_in_range
from ts_text_coords import (
    char_index_from_line_col,
    flat_index_to_raw_index,
    is_comment_line,
    line_col_from_char_index,
    raw_index_to_flat_index,
)


@dataclass(frozen=True)
class LocateOutcome:
    """Phase-2 result.

    On failure, ``ok`` is False and ``result["error"]`` is set.
    On success, ``context.callee_location`` is populated.
    """

    result: Dict[str, Any]
    context: ResolutionContext

    @property
    def ok(self) -> bool:
        return self.context.callee_location is not None


@dataclass
class TsCalleeMatch:
    """One AST-derived candidate for the callee (line0, col0 are 0-based)."""

    line0: int
    col0: int
    expr_src: str
    node_line0: int = 0


def _symbol_identifier_pattern(symbol_name: str) -> str:
    esc = re.escape(symbol_name)
    if symbol_name.startswith("$"):
        return rf"(?<![\w$]){esc}(?![\w$])"
    return rf"(?<![\w$\.]){esc}(?![\w$])"


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
    # Collapse call argument lists so snippet `foo()` matches AST `foo(1)`.
    while True:
        nxt = re.sub(r"\([^()]*\)", "()", s)
        if nxt == s:
            break
        s = nxt
    return s


def expr_src_offset_for_selector_name(expr_src: str, selector: SnippetSelector) -> int:
    """Offset from start of expr_src to the callee identifier."""
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
        dotted = list(re.finditer(r"\." + esc + r"(?:\s*[\(<]|\s*$)", expr_src))
        if dotted:
            return dotted[0].start() + 1
        m = re.search(_symbol_identifier_pattern(name) + r"(?:\s*[\(<]|\s*$)", expr_src)
        if m:
            return m.start()
    elif selector.kind == "attr":
        dotted = list(re.finditer(r"\." + esc + r"\b", expr_src))
        if dotted:
            return dotted[0].start() + 1
    idx = expr_src.find(name)
    return idx if idx >= 0 else 0


def clamp_position_to_source(text: str, line0: int, col0: int) -> Tuple[int, int]:
    lines_list = text.splitlines()
    if not lines_list:
        return 0, 0
    line0 = max(0, min(int(line0), len(lines_list) - 1))
    line_len = len(lines_list[line0])
    col0 = max(0, min(int(col0), line_len))
    return line0, col0


def _walk_ts_find_callees(
    node,
    source_bytes: bytes,
    tested_rng: Optional[TestedRange],
    selector: SnippetSelector,
    out: List[TsCalleeMatch],
) -> None:
    if node is None:
        return

    if selector.kind == "call" and node.type == "call_expression":
        func = node.child_by_field_name("function")
        if func is not None:
            name_node = None
            recv_src: Optional[str] = None
            if func.type == "identifier":
                name = node_text(source_bytes, func)
                if name == selector.name and selector.receiver is None:
                    name_node = func
            elif func.type == "member_expression":
                prop = func.child_by_field_name("property")
                if prop is not None:
                    name = node_text(source_bytes, prop)
                    if name == selector.name:
                        obj = func.child_by_field_name("object")
                        recv_src = node_text(source_bytes, obj).strip() if obj else None
                        if selector.receiver is None or (
                            recv_src
                            and _normalize_anchor_for_exact_match(recv_src)
                            == _normalize_anchor_for_exact_match(selector.receiver or "")
                        ):
                            name_node = prop
            if name_node is not None:
                r, c = name_node.start_point
                if point_in_range(r, c, tested_rng):
                    out.append(
                        TsCalleeMatch(
                            line0=r,
                            col0=c,
                            expr_src=node_text(source_bytes, node),
                            node_line0=node.start_point[0],
                        )
                    )

    if selector.kind == "attr" and node.type == "member_expression":
        prop = node.child_by_field_name("property")
        if prop is not None:
            name = node_text(source_bytes, prop)
            if name == selector.name:
                obj = node.child_by_field_name("object")
                recv_src = node_text(source_bytes, obj).strip() if obj else None
                if selector.receiver is None or (
                    recv_src
                    and _normalize_anchor_for_exact_match(recv_src)
                    == _normalize_anchor_for_exact_match(selector.receiver or "")
                ):
                    r, c = prop.start_point
                    if point_in_range(r, c, tested_rng):
                        out.append(
                            TsCalleeMatch(
                                line0=r,
                                col0=c,
                                expr_src=node_text(source_bytes, node),
                                node_line0=node.start_point[0],
                            )
                        )

    for i in range(node.child_count):
        _walk_ts_find_callees(node.child(i), source_bytes, tested_rng, selector, out)


def find_ts_callee_nodes_ast(
    source: str,
    tested_rng: Optional[TestedRange],
    selector: SnippetSelector,
    script_path: Path,
) -> List[TsCalleeMatch]:
    parser = get_ts_parser(script_path)
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


def extract_tested_function_range_ts_ast(
    source: str,
    function_name: str,
    script_path: Path,
) -> Optional[TestedRange]:
    parser = get_ts_parser(script_path)
    if parser is None:
        return None
    try:
        source_bytes = source.encode("utf-8")
        tree = parser.parse(source_bytes)
    except Exception:
        return None
    if tree.root_node is None or tree.root_node.has_error:
        return None

    def walk(node) -> Optional[TestedRange]:
        if node.type in ("function_declaration", "method_definition", "generator_function"):
            name_node = node.child_by_field_name("name")
            if name_node is not None and node_text(source_bytes, name_node) == function_name:
                sl, sc = node.start_point
                el, ec = node.end_point
                return (int(sl), int(sc), int(el), int(ec))
        for i in range(node.child_count):
            found = walk(node.child(i))
            if found is not None:
                return found
        return None

    return walk(tree.root_node)


def filter_by_anchor_strict_ts(
    script_lines: List[str],
    candidates: List[TsCalleeMatch],
    anchor: str,
    window: int,
) -> List[TsCalleeMatch]:
    anchor_n = _normalize_anchor_for_exact_match(anchor)
    exact = [
        m
        for m in candidates
        if anchor_n == _normalize_anchor_for_exact_match(m.expr_src)
    ]
    if exact:
        return exact
    contained = [
        m
        for m in candidates
        if anchor_n and anchor_n in _normalize_anchor_for_exact_match(m.expr_src)
    ]
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


def _find_anchor_candidates_in_range(
    source: str,
    anchor: str,
    *,
    tested_rng: Optional[TestedRange],
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

    if "\n" in anchor or "\r" in anchor:
        start_i = char_index_from_line_col(source, lo, 0)
        if hi + 1 < len(lines):
            end_i = char_index_from_line_col(source, hi + 1, 0)
        else:
            end_i = len(source)
        out_m: List[Tuple[int, int, str]] = []
        pos = source.find(anchor, start_i, end_i)
        while pos >= 0:
            line0, col0 = line_col_from_char_index(source, pos)
            line_text = lines[line0] if 0 <= line0 < len(lines) else ""
            out_m.append((line0, col0, line_text))
            pos = source.find(anchor, pos + 1, end_i)
        if out_m or "\r\n" not in source:
            return out_m
        flat = source.replace("\r\n", "\n")
        s_f = raw_index_to_flat_index(source, start_i)
        e_f = raw_index_to_flat_index(source, min(end_i, len(source)))
        pos_f = flat.find(anchor, s_f, e_f)
        while pos_f >= 0:
            raw = flat_index_to_raw_index(source, pos_f)
            line0, col0 = line_col_from_char_index(source, raw)
            line_text = lines[line0] if 0 <= line0 < len(lines) else ""
            out_m.append((line0, col0, line_text))
            pos_f = flat.find(anchor, pos_f + 1, e_f)
        return out_m

    out: List[Tuple[int, int, str]] = []
    for line0 in range(lo, hi + 1):
        line = lines[line0]
        if is_comment_line(line):
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
    tested_rng: Optional[TestedRange],
) -> List[Tuple[int, int, str]]:
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
        pattern = name + "("
        alt_pattern = "." + name + "("
    else:
        pattern = name
        alt_pattern = "." + name

    for line0 in range(lo, hi + 1):
        line = lines[line0]
        if is_comment_line(line):
            continue
        idx = line.find(alt_pattern)
        if idx >= 0:
            col0 = idx + 1
        else:
            idx = line.find(pattern)
            col0 = idx
        if idx >= 0:
            out.append((line0, col0, line))
    return out


def pick_anchor_candidates_with_fallbacks(
    text: str,
    anchor_text: str,
    selector: SnippetSelector,
    tested_rng: Optional[TestedRange],
) -> List[Tuple[int, int, str, bool]]:
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
            in_range = [
                (line0, col0, lt)
                for line0, col0, lt in candidates
                if start_line <= line0 <= end_line
            ]
            if in_range:
                return [(in_range[0][0], in_range[0][1], in_range[0][2], True)]
        one = candidates[0]
        return [(one[0], one[1], one[2], True)]
    candidates = _find_anchor_candidates_by_core(text, selector, tested_rng=None)
    if candidates:
        if tested_rng is not None and len(candidates) > 1:
            start_line, _, end_line, _ = tested_rng
            in_range = [
                (line0, col0, lt)
                for line0, col0, lt in candidates
                if start_line <= line0 <= end_line
            ]
            if in_range:
                return [(in_range[0][0], in_range[0][1], in_range[0][2], True)]
        one = candidates[0]
        return [(one[0], one[1], one[2], True)]
    return []


def _match_snippet_for_nested_offsets(
    text: str,
    snippet: str,
    alternatives: List[str],
    hint_index: int,
) -> Optional[Tuple[int, bool]]:
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
    hint_f = raw_index_to_flat_index(text, min(hint_index, len(text)))
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


def nested_usage_to_file_line_col(
    text: str,
    snippet: str,
    outer_line0: int,
    outer_anchor_col0: int,
    offset_in_snippet: int,
    expr_src_alt: str,
) -> Tuple[int, int]:
    """Map offset within the callee snippet string to (line0, col0) in the file."""
    if "\n" not in snippet and "\r" not in snippet:
        return outer_line0, outer_anchor_col0 + offset_in_snippet
    hint = char_index_from_line_col(text, outer_line0, outer_anchor_col0)
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
        target = flat_index_to_raw_index(text, tf)
    else:
        target = start + offset_in_snippet
        if target < 0 or target > len(text):
            return outer_line0, outer_anchor_col0 + offset_in_snippet
    return line_col_from_char_index(text, target)


def _navigation_position(
    *,
    text: str,
    selector: SnippetSelector,
    search_text: str,
    match_pos: Position,
    expr_src: str,
    pattern: str,
) -> Position:
    line0 = match_pos.line0
    anchor_col0 = match_pos.col0
    if pattern in ("ast", "core_fallback"):
        col0 = anchor_col0
    else:
        rel_idx = expr_src_offset_for_selector_name(expr_src, selector)
        if "\n" in expr_src or "\r" in expr_src:
            line0, col0 = nested_usage_to_file_line_col(
                text,
                expr_src,
                line0,
                anchor_col0,
                rel_idx,
                search_text,
            )
        else:
            col0 = anchor_col0 + rel_idx if rel_idx >= 0 else anchor_col0
    line0, col0 = clamp_position_to_source(text, line0, col0)
    return Position(line0=line0, col0=col0)


def _line_text(script_lines: List[str], line0: int) -> str:
    return script_lines[line0] if 0 <= line0 < len(script_lines) else ""


def locate_callee(ctx: ResolutionContext, result: Dict[str, Any]) -> LocateOutcome:
    """Run phase 2: find the callee usage and set navigation on ctx + result."""
    text = ctx.text
    script_path = ctx.file_path
    selector = ctx.selector
    search_text = ctx.search_text
    window = ctx.window
    script_lines = text.splitlines()
    path_str = str(script_path)

    tested_rng: Optional[TestedRange] = None
    if ctx.tested_function:
        tested_rng = extract_tested_function_range_ts_ast(
            text, ctx.tested_function, script_path
        )
    ctx.expr_rng = tested_rng

    candidates: List[Dict[str, Any]] = []
    anchored: List[Dict[str, Any]] = []
    chosen: Optional[Dict[str, Any]] = None
    pattern = ""
    match_pos: Optional[Position] = None
    expr_src = search_text

    if TREE_SITTER_AVAILABLE:
        usage_candidates = find_ts_callee_nodes_ast(
            text, tested_rng, selector, script_path
        )
        if usage_candidates:
            strict = filter_by_anchor_strict_ts(
                script_lines, usage_candidates, search_text, window
            )
            if strict:
                pattern = "ast"
                m = strict[0]
                match_pos = Position(line0=m.line0, col0=m.col0)
                expr_src = m.expr_src
                chosen = build_match_entry(
                    selector=selector,
                    pos=match_pos,
                    path=path_str,
                    expr_src=expr_src,
                    pattern=pattern,
                    line_text=_line_text(script_lines, m.line0),
                )
                candidates = [
                    build_match_entry(
                        selector=selector,
                        pos=Position(line0=c.line0, col0=c.col0),
                        path=path_str,
                        expr_src=c.expr_src,
                        pattern=pattern,
                        line_text=_line_text(script_lines, c.line0),
                    )
                    for c in usage_candidates
                ]
                anchored = [chosen]

    if chosen is None:
        raw = pick_anchor_candidates_with_fallbacks(
            text, search_text, selector, tested_rng
        )
        if not raw:
            return LocateOutcome(
                result=build_failure_result(
                    result,
                    error=(
                        "No candidates found by anchor inside tested_function "
                        "(or file if range unknown)."
                    ),
                ),
                context=ctx,
            )
        candidates = []
        for line0, col0, line_text, from_core in raw:
            pat = "core_fallback" if from_core else "anchor_substring"
            candidates.append(
                build_match_entry(
                    selector=selector,
                    pos=Position(line0=line0, col0=col0),
                    path=path_str,
                    expr_src=search_text,
                    pattern=pat,
                    line_text=line_text,
                )
            )
        anchored = list(candidates)
        chosen = anchored[0]
        pattern = chosen["meta"]["pattern"]
        match_pos = Position(
            line0=chosen["ref"]["line0"],
            col0=chosen["ref"]["col0"],
        )
        expr_src = chosen.get("expr_src") or search_text

    if chosen is None or match_pos is None:
        return LocateOutcome(
            result=build_failure_result(
                result, error="No matching callee found for this snippet."
            ),
            context=ctx,
        )

    navigation = _navigation_position(
        text=text,
        selector=selector,
        search_text=search_text,
        match_pos=match_pos,
        expr_src=expr_src,
        pattern=pattern,
    )
    ctx.callee_location = CalleeLocation(
        match=match_pos,
        callee_start=navigation,
        expr_src=expr_src,
        pattern=pattern,
        expr_rng=tested_rng,
    )
    apply_callee_to_result(
        result,
        candidates=candidates,
        chosen=chosen,
        navigation=navigation,
        anchored=anchored,
    )
    return LocateOutcome(result=result, context=ctx)
