"""Locate a TypeScript/JavaScript callee in the usage file (phase 2).

Given a prepared ResolutionContext, find the usage site via tree-sitter AST,
compute the navigation cursor, and write:

  - ctx.expr_rng / ctx.callee_location
  - result["matches"] / result["navigation_position"]

If tree-sitter is unavailable or no AST match is found, locate fails with an error
(no text/substring fallback).
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
    """One AST-derived candidate for the callee"""

    line0: int
    col0: int
    expr_src: str
    node_line0: int = 0


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


def clamp_position_to_source(text: str, line0: int, col0: int) -> Tuple[int, int]:
    lines_list = text.splitlines()
    if not lines_list:
        return 0, 0
    line0 = max(0, min(int(line0), len(lines_list) - 1))
    line_len = len(lines_list[line0])
    col0 = max(0, min(int(col0), line_len))
    return line0, col0


def _walk_ts_find_first_callee(
    node,
    source_bytes: bytes,
    tested_rng: Optional[TestedRange],
    selector: SnippetSelector,
) -> Optional[TsCalleeMatch]:
    if node is None:
        return None

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
                    return TsCalleeMatch(
                        line0=r,
                        col0=c,
                        expr_src=node_text(source_bytes, node),
                        node_line0=node.start_point[0],
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
                        return TsCalleeMatch(
                            line0=r,
                            col0=c,
                            expr_src=node_text(source_bytes, node),
                            node_line0=node.start_point[0],
                        )

    for i in range(node.child_count):
        found = _walk_ts_find_first_callee(
            node.child(i), source_bytes, tested_rng, selector
        )
        if found is not None:
            return found
    return None


def find_ts_callee_node_ast(
    source: str,
    tested_rng: Optional[TestedRange],
    selector: SnippetSelector,
    script_path: Path,
) -> Optional[TsCalleeMatch]:
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
    return _walk_ts_find_first_callee(
        tree.root_node, source_bytes, tested_rng, selector
    )


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


def _navigation_position(*, text: str, match_pos: Position) -> Position:
    """AST hits already point at the identifier; just clamp to file bounds."""
    line0, col0 = clamp_position_to_source(text, match_pos.line0, match_pos.col0)
    return Position(line0=line0, col0=col0)


def _line_text(script_lines: List[str], line0: int) -> str:
    return script_lines[line0] if 0 <= line0 < len(script_lines) else ""


def locate_callee(ctx: ResolutionContext, result: Dict[str, Any]) -> LocateOutcome:
    """Run phase 2: find the callee usage via AST and set navigation on ctx + result."""
    if not TREE_SITTER_AVAILABLE:
        return LocateOutcome(
            result=build_failure_result(result, error="Callee not found."),
            context=ctx,
        )

    text = ctx.text
    script_path = ctx.file_path
    selector = ctx.selector
    script_lines = text.splitlines()
    path_str = str(script_path)

    tested_rng: Optional[TestedRange] = None
    if ctx.tested_function:
        tested_rng = extract_tested_function_range_ts_ast(
            text, ctx.tested_function, script_path
        )
    ctx.expr_rng = tested_rng

    m = find_ts_callee_node_ast(text, tested_rng, selector, script_path)
    if m is None:
        return LocateOutcome(
            result=build_failure_result(result, error="Callee not found."),
            context=ctx,
        )

    match_pos = Position(line0=m.line0, col0=m.col0)
    chosen = build_match_entry(
        selector=selector,
        pos=match_pos,
        path=path_str,
        expr_src=m.expr_src,
        pattern="ast",
        line_text=_line_text(script_lines, m.line0),
    )
    navigation = _navigation_position(text=text, match_pos=match_pos)
    ctx.callee_location = CalleeLocation(
        match=match_pos,
        callee_start=navigation,
        expr_src=m.expr_src,
        pattern="ast",
        expr_rng=tested_rng,
    )
    apply_callee_to_result(
        result,
        candidates=[chosen],
        chosen=chosen,
        navigation=navigation,
        anchored=[chosen],
    )
    return LocateOutcome(result=result, context=ctx)
