#!/usr/bin/env python3
"""
Run code_navigation_TypeScript on every qualifying call/attribute in each hoppscotch.json sample.

For each extracted callee snippet, writes one JSON row that is the full return value of
code_navigation_TypeScript.resolve_from_snippet, plus eval metadata (sample_id, callee_index,
tested_function, script_path, callee). No merged per-sample record — results are flat and
match the TypeScript navigator shape for easier debugging.

Qualifying callees = (1) outside calls, (2) outside attribute access (see extract_all_callees).
Samples whose body has no such callees are omitted from the output (no error row).

Expects a clone of Hoppscotch at commit f8cd8bf (or compatible layout) at ./hoppscotch.

Usage:
  python run_n8n_code_navigation_eval.py                    # run all
  python run_n8n_code_navigation_eval.py --limit 10         # run first 10 samples only
  python run_n8n_code_navigation_eval.py -o eval_output.txt  # write summary to this file
  python run_n8n_code_navigation_eval.py --results-json hoppscotch_eval_results_b.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
DOCPRISM_ROOT = SCRIPT_DIR
HOPPSCOTCH_REPO_ROOT = DOCPRISM_ROOT / "hoppscotch"
EVAL_JSON = DOCPRISM_ROOT / "hoppscotch.json"

HOPPSCOTCH_PATH_PREFIX = "/Users/kyle/Documents/ubc/research/data/ts/hoppscotch/"


def load_eval_set(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _skip_generics(text: str, pos: int) -> int:
    """If text[pos:] starts with <...>, return index after the matching '>'. Else return pos."""
    i = pos
    while i < len(text) and text[i] in " \t":
        i += 1
    if i >= len(text) or text[i] != "<":
        return pos
    depth = 1  # we're inside the opening <
    i += 1
    while i < len(text):
        if text[i] == "<":
            depth += 1
        elif text[i] == ">":
            depth -= 1
            if depth == 0:
                return i + 1
        elif text[i] in '"\'':
            quote = text[i]
            i += 1
            while i < len(text) and text[i] != quote:
                i += 2 if text[i] == "\\" else 1
            i += 1
            continue
        i += 1
    return pos


def extract_tested_function(code: str) -> str | None:
    """Extract the function/method name from the code snippet."""
    code = code.strip()
    # function name( or async function name(
    m = re.match(r"(?:async\s+)?function\s+(\w+)\s*\(", code)
    if m:
        return m.group(1)
    m = re.match(r"function\s+(\w+)\s*\(", code)
    if m:
        return m.group(1)
    # Method: optional modifiers in any order (async, public, protected, private, static), then name, optional generics, then (
    m = re.match(r"(?:(?:async|public|protected|private|static)\s+)*(\w+)", code)
    if m:
        name = m.group(1)
        rest_pos = _skip_generics(code, m.end())
        if rest_pos < len(code) and re.match(r"\s*\(", code[rest_pos:]):
            return name
    # getter: get name()
    m = re.match(r"get\s+(\w+)\s*\(\s*\)", code)
    if m:
        return m.group(1)
    # setter: set name(
    m = re.match(r"set\s+(\w+)\s*\(", code)
    if m:
        return m.group(1)
    return None


def _collapse_call_arguments(call: str) -> str:
    """
    Replace bulky multiline/literal/callback arguments with ``...`` so callee
    extraction stays at the call boundary (e.g. ``prisma.$transaction(...)``).
    """
    open_paren = call.find("(")
    if open_paren == -1:
        return call
    close = _find_matching_closing_paren(call, open_paren)
    if close is None:
        return call
    inner = call[open_paren + 1 : close].strip()
    if not inner:
        return call
    if "\n" in call[open_paren : close + 1]:
        return call[: open_paren + 1] + "...)"
    if inner[0] in "{[":
        return call[: open_paren + 1] + "...)"
    if inner.startswith("async ") or inner.startswith("function"):
        return call[: open_paren + 1] + "...)"
    return call


def _find_matching_closing_paren(text: str, open_pos: int) -> int | None:
    """Return index of the ')' that matches the '(' at open_pos, or None."""
    depth = 0
    i = open_pos
    while i < len(text):
        ch = text[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        elif ch in '"\'':
            # Skip string literals so we don't count parens inside them
            quote = ch
            i += 1
            while i < len(text):
                if text[i] == "\\":
                    i += 2
                    continue
                if text[i] == quote:
                    i += 1
                    break
                i += 1
            continue  # Next iteration will process character at i; don't skip it
        elif ch == "`":
            i = _scan_past_template_literal(text, i)
            continue
        i += 1
    return None


def _scan_past_string(body: str, i: int, quote: str) -> int:
    n = len(body)
    i += 1
    while i < n:
        if body[i] == "\\":
            i += 2
            continue
        if body[i] == quote:
            return i + 1
        i += 1
    return n


def _scan_past_template_expr(body: str, i: int) -> int:
    n = len(body)
    depth = 1
    while i < n and depth > 0:
        ch = body[i]
        if ch in "'\"":
            i = _scan_past_string(body, i, ch)
            continue
        if ch == "`":
            i = _scan_past_template_literal(body, i)
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        i += 1
    return i


def _scan_past_template_literal(body: str, start_backtick: int) -> int:
    n = len(body)
    i = start_backtick + 1
    while i < n:
        ch = body[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "`":
            return i + 1
        if ch == "$" and i + 1 < n and body[i + 1] == "{":
            i = _scan_past_template_expr(body, i + 2)
            continue
        i += 1
    return n


def _extract_local_names(code: str, tested_function: str) -> set[str]:
    """
    Extract names that are local to the function (params + names defined in body).
    These are excluded when finding 'outside' calls/attributes.
    """
    lines = code.split("\n")
    first_line = lines[0] if lines else ""
    body = "\n".join(lines[1:]) if len(lines) > 1 else ""
    locals_set: set[str] = {tested_function}

    # Parameter names from first line: between first ( and matching )
    paren_open = first_line.find("(")
    if paren_open != -1:
        close = _find_matching_closing_paren(first_line, paren_open)
        if close is not None:
            params_str = first_line[paren_open + 1 : close]
            # Simple param names (identifier, or identifier: type, or ...rest)
            for part in re.split(r"[,=]", params_str):
                part = part.strip()
                # Skip rest/spread
                if part.startswith("..."):
                    part = part[3:].strip()
                m = re.match(r"([A-Za-z_$][A-Za-z0-9_$]*)", part)
                if m:
                    locals_set.add(m.group(1))

    # Names defined in body: function name(, const/let/var name
    # Nested function declarations
    for m in re.finditer(r"(?:async\s+)?function\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*\(", body):
        locals_set.add(m.group(1))
    for m in re.finditer(r"\b(?:const|let|var)\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*[=:]", body):
        locals_set.add(m.group(1))
    # for (const x of ...) or for (let x of ...)
    for m in re.finditer(r"\bfor\s*\(\s*(?:const|let)\s+([A-Za-z_$][A-Za-z0-9_$]*)", body):
        locals_set.add(m.group(1))

    locals_set.update(_extract_arrow_callback_param_names(body))

    return locals_set


# Keywords that are not callees (e.g. async (x) => ... is a callback, not a call)
_CALL_SKIP_KEYWORDS = frozenset(
    (
        "if",
        "for",
        "while",
        "switch",
        "catch",
        "return",
        "typeof",
        "new",
        "async",   # async (params) => ... is an arrow function, not a call
        "function",  # function (...) is a declaration/anonymous expr, not a call
    )
)


def _is_for_of_iterator_of_keyword(body: str, of_keyword_start: int) -> bool:
    if of_keyword_start < 0 or of_keyword_start + 2 > len(body):
        return False
    if body[of_keyword_start : of_keyword_start + 2] != "of":
        return False
    before = of_keyword_start > 0 and (
        body[of_keyword_start - 1].isalnum() or body[of_keyword_start - 1] == "_"
    )
    after = of_keyword_start + 2 < len(body) and (
        body[of_keyword_start + 2].isalnum() or body[of_keyword_start + 2] == "_"
    )
    if before or after:
        return False
    i = of_keyword_start - 1
    while i >= 0 and body[i] in " \t":
        i -= 1
    paren_depth = 0
    bracket_depth = 0
    brace_depth = 0
    while i >= 0:
        ch = body[i]
        if ch == ")":
            paren_depth += 1
        elif ch == "(":
            if paren_depth > 0:
                paren_depth -= 1
            elif bracket_depth > 0 or brace_depth > 0:
                pass
            else:
                inner = body[i + 1 : of_keyword_start]
                if not re.search(r"\b(?:const|let|var)\s+", inner):
                    i -= 1
                    continue
                head = body[:i].rstrip()
                if head.endswith("for") or re.search(r"\bfor\s+await\s*$", head):
                    return True
        elif ch == "]":
            bracket_depth += 1
        elif ch == "[":
            if bracket_depth > 0:
                bracket_depth -= 1
        elif ch == "}":
            brace_depth += 1
        elif ch == "{":
            if brace_depth > 0:
                brace_depth -= 1
        i -= 1
    return False


def _is_inside_string_literal(body: str, pos: int) -> bool:
    """
    True if pos is inside non-code text: '...', "...", or template literal text
    (outside ${...}).
    """
    if pos < 0 or pos >= len(body):
        return False
    i = 0
    n = len(body)
    while i < pos:
        ch = body[i]
        if ch == "'":
            j = _scan_past_string(body, i, "'")
            if j > pos:
                return True
            i = j
            continue
        if ch == '"':
            j = _scan_past_string(body, i, '"')
            if j > pos:
                return True
            i = j
            continue
        if ch == "`":
            i += 1
            while i < pos:
                c = body[i]
                if c == "\\":
                    i += 2
                    continue
                if c == "`":
                    i += 1
                    break
                if c == "$" and i + 1 < n and body[i + 1] == "{":
                    expr_end = _scan_past_template_expr(body, i + 2)
                    if pos < expr_end:
                        return False
                    i = expr_end
                    continue
                i += 1
            else:
                return True
            continue
        i += 1
    return False


def _top_level_commas_split(params: str) -> list[str]:
    parts: list[str] = []
    pr = brk = br = 0
    start = 0
    for i, ch in enumerate(params):
        if ch == "(":
            pr += 1
        elif ch == ")":
            pr -= 1
        elif ch == "[":
            brk += 1
        elif ch == "]":
            brk -= 1
        elif ch == "{":
            br += 1
        elif ch == "}":
            br -= 1
        elif ch == "," and pr == 0 and brk == 0 and br == 0:
            parts.append(params[start:i].strip())
            start = i + 1
    parts.append(params[start:].strip())
    return [p for p in parts if p]


def _param_name_from_chunk(chunk: str) -> Optional[str]:
    chunk = chunk.strip()
    if not chunk:
        return None
    if chunk.startswith("..."):
        chunk = chunk[3:].strip()
    if chunk.startswith("{") or chunk.startswith("["):
        return None
    m = re.match(r"^([A-Za-z_$][\w$]*)", chunk)
    return m.group(1) if m else None


def _extract_arrow_callback_param_names(body: str) -> set[str]:
    names: set[str] = set()
    for m in re.finditer(r"\)\s*=>", body):
        close_idx = m.start()
        depth = 0
        j = close_idx
        while j >= 0:
            if body[j] == ")":
                depth += 1
            elif body[j] == "(":
                depth -= 1
                if depth == 0:
                    inner = body[j + 1 : close_idx]
                    for part in _top_level_commas_split(inner):
                        nm = _param_name_from_chunk(part)
                        if nm:
                            names.add(nm)
                    break
            j -= 1
    return names


def extract_all_callees(code: str, tested_function: str) -> list[str]:
    """
    Extract all callees from the function body that are 'outside':
    1) Function calls where the called name is defined outside (another file, API, library).
    2) Attribute/property access where the receiver is defined outside.
    Excludes calls to the tested function itself and to names defined locally
    (params, nested functions, const/let/var in the body).
    Returns a list of unique snippets (full call or recv.prop) to resolve.
    """
    lines = code.split("\n")
    body = "\n".join(lines[1:]) if len(lines) > 1 else code
    local_names = _extract_local_names(code, tested_function)
    seen: set[str] = set()

    def is_outside_root(name: str) -> bool:
        return name not in local_names and name != tested_function

    result: list[str] = []

    # 1) Chained calls: obj.method(...) or obj.a.b.method(...)
    chained_re = re.compile(r"([A-Za-z_$][A-Za-z0-9_$]*(?:\.[A-Za-z_$][A-Za-z0-9_$]*)+\s*\()")
    for m in chained_re.finditer(body):
        if _is_inside_string_literal(body, m.start(0)):
            continue
        start, end = m.start(1), m.end(1)
        root_name = m.group(1).split(".")[0].strip()
        if not is_outside_root(root_name):
            continue
        open_paren = body.find("(", end - 1)
        if open_paren == -1:
            continue
        close = _find_matching_closing_paren(body, open_paren)
        if close is None:
            continue
        callee = _collapse_call_arguments(body[start : close + 1].strip())
        if callee in seen:
            continue
        seen.add(callee)
        result.append(callee)

    # 2) Plain function calls: name(  (exclude method calls like .name( and comments)
    call_re = re.compile(r"\b([A-Za-z_$][A-Za-z0-9_$]*)\s*\(")
    for m in call_re.finditer(body):
        if _is_inside_string_literal(body, m.start(0)):
            continue
        # Skip method / $-prefixed calls — already captured as chained callees
        if m.start(0) > 0 and body[m.start(0) - 1] in ".$":
            continue
        # Skip if inside a line comment
        line_start = body.rfind("\n", 0, m.start(0)) + 1
        line = body[line_start : body.find("\n", m.start(0)) if body.find("\n", m.start(0)) != -1 else len(body)]
        if "//" in line and line.index("//") < m.start(0) - line_start:
            continue
        if line.strip().startswith("//"):
            continue
        name = m.group(1)
        if name in _CALL_SKIP_KEYWORDS or not is_outside_root(name):
            continue
        if name == "of" and _is_for_of_iterator_of_keyword(body, m.start(1)):
            continue
        open_paren = m.start(0) + len(m.group(1))
        while open_paren < len(body) and body[open_paren] in " \t":
            open_paren += 1
        if open_paren >= len(body) or body[open_paren] != "(":
            continue
        close = _find_matching_closing_paren(body, open_paren)
        if close is None:
            continue
        callee = _collapse_call_arguments(body[m.start(0) : close + 1].strip())
        if callee in seen:
            continue
        seen.add(callee)
        result.append(callee)

    # 3) Property/attribute access: recv.prop where recv is outside (e.g. this, or outer name)
    # Skip when inside a comment or string
    attr_re = re.compile(r"([A-Za-z_$][A-Za-z0-9_$]*)\s*\.\s*([A-Za-z_$][A-Za-z0-9_$]*)")
    for m in attr_re.finditer(body):
        if _is_inside_string_literal(body, m.start(0)):
            continue
        line_start = body.rfind("\n", 0, m.start(0)) + 1
        line = body[line_start : body.find("\n", m.start(0)) if body.find("\n", m.start(0)) != -1 else len(body)]
        if "//" in line and line.index("//") < m.start(0) - line_start:
            continue
        if line.strip().startswith("//"):
            continue
        recv, prop = m.group(1), m.group(2)
        if recv in local_names:
            continue
        full = f"{recv}.{prop}"
        if full in seen:
            continue
        # Skip if we already extracted this as a method call (e.g. cy.intercept(...))
        if any(s.startswith(full + "(") for s in seen):
            continue
        seen.add(full)
        result.append(full)

    return result


def extract_first_callee(code: str, tested_function: str) -> str | None:
    """
    Extract a callee from the function body to resolve.
    Returns a fully wrapped call snippet including arguments and closing paren)
    """
    lines = code.split("\n")
    body = "\n".join(lines[1:]) if len(lines) > 1 else code
    local_names = _extract_local_names(code, tested_function)

    # Prefer chained call: obj.method(...) or obj.a.b.method(...)
    m = re.search(r"([A-Za-z_$][A-Za-z0-9_$]*(?:\.[A-Za-z_$][A-Za-z0-9_$]*)+\s*\()", body)
    if m and not _is_inside_string_literal(body, m.start(1)):
        start, end = m.start(1), m.end(1)
        open_paren = body.find("(", end - 1)
        if open_paren != -1:
            close = _find_matching_closing_paren(body, open_paren)
            if close is not None:
                callee = body[start : close + 1].strip()
                if not callee.startswith(tested_function + "("):
                    return callee

    # Plain call
    call_re = re.compile(r"\b([A-Za-z_$][A-Za-z0-9_$]*)\s*\(")
    for m in call_re.finditer(body):
        if _is_inside_string_literal(body, m.start(0)):
            continue
        name = m.group(1)
        if name in ("if", "for", "while", "switch", "catch", "return", "typeof", "new"):
            continue
        if name == "of" and _is_for_of_iterator_of_keyword(body, m.start(1)):
            continue
        if name == tested_function:
            continue
        open_paren = m.start(0) + len(m.group(1))
        while open_paren < len(body) and body[open_paren] in " \t":
            open_paren += 1
        if open_paren < len(body) and body[open_paren] == "(":
            close = _find_matching_closing_paren(body, open_paren)
            if close is not None:
                return body[m.start(0) : close + 1].strip()
        return name + "("

    # Property access
    attr_re = re.compile(r"([A-Za-z_$][A-Za-z0-9_$]*)\s*\.\s*([A-Za-z_$][A-Za-z0-9_$]*)")
    for m in attr_re.finditer(body):
        if _is_inside_string_literal(body, m.start(0)):
            continue
        recv, prop = m.group(1), m.group(2)
        if recv in local_names:
            continue
        if recv == "this":
            return f"this.{prop}"
        full = f"{recv}.{prop}"
        if full != tested_function:
            return full

    return None


def json_filename_to_local_path(filename: str) -> Path:
    """Convert absolute path from JSON to local path."""
    if filename.startswith(HOPPSCOTCH_PATH_PREFIX):
        rel = filename[len(HOPPSCOTCH_PATH_PREFIX) :]
    else:
        if "/hoppscotch/" in filename:
            rel = filename.split("/hoppscotch/", 1)[1]
        else:
            rel = Path(filename).name
    return HOPPSCOTCH_REPO_ROOT / rel


def _stub_resolve_shape(
    *,
    error: str,
    tested_function: str = "",
    script_path_str: str = "",
    snippet: str = "",
) -> Dict[str, Any]:
    """Same top-level keys as resolve_from_snippet when navigation never ran."""
    return {
        "ok": False,
        "input": {
            "repo_root": str(HOPPSCOTCH_REPO_ROOT),
            "script_path": script_path_str,
            "tested_function": tested_function,
            "snippet": snippet,
            "anchor": snippet,
            "usage": {"kind": "call", "receiver": None, "name": ""},
            "selector": {"anchor": snippet, "window": 3},
        },
        "error": error,
        "matches": {"candidates": [], "anchored": [], "chosen": None},
        "definitions_all": [],
        "definitions_all_filtered": [],
        "chosen_definition_reason": None,
        "definitions": [],
    }


def _eval_sample(item: dict) -> List[dict]:
    """
    Evaluate one hoppscotch.json sample: extract callees, run resolve_from_snippet on each.
    Returns one dict per callee — each dict is eval metadata plus the full navigator output.

    Defined at module top level for ProcessPoolExecutor (imports inside worker).
    """
    sys.path.insert(0, str(DOCPRISM_ROOT))
    from code_navigation_TypeScript import resolve_from_snippet

    eid = item.get("id", "?")
    filename = item.get("filename", "")
    code = item.get("code", "")
    script_path = json_filename_to_local_path(filename)

    def one_row(
        *,
        callee_index: int,
        tested_function: Optional[str],
        callee: Optional[str],
        navigation: Dict[str, Any],
    ) -> dict:
        return {
            "sample_id": eid,
            "callee_index": callee_index,
            "tested_function": tested_function,
            "script_path": str(script_path) if script_path else None,
            "callee": callee,
            **navigation,
        }

    if not code:
        return [
            one_row(
                callee_index=0,
                tested_function=None,
                callee=None,
                navigation=_stub_resolve_shape(error="missing code"),
            )
        ]

    tested_function = extract_tested_function(code)
    if not tested_function:
        return [
            one_row(
                callee_index=0,
                tested_function=None,
                callee=None,
                navigation=_stub_resolve_shape(error="could not extract tested_function"),
            )
        ]

    callees = extract_all_callees(code, tested_function)
    if not callees:
        return []

    if not script_path.exists():
        return [
            one_row(
                callee_index=0,
                tested_function=tested_function,
                callee=callees[0],
                navigation=_stub_resolve_shape(
                    error=f"file not found: {script_path}",
                    tested_function=tested_function,
                    script_path_str=str(script_path),
                    snippet=callees[0],
                ),
            )
        ]

    rows: List[dict] = []
    for idx, callee in enumerate(callees):
        try:
            res = resolve_from_snippet(
                repo_root=HOPPSCOTCH_REPO_ROOT,
                script_path=script_path,
                tested_function=tested_function,
                snippet=callee,
                anchor=callee,
            )
            rows.append(
                one_row(
                    callee_index=idx,
                    tested_function=tested_function,
                    callee=callee,
                    navigation=res,
                )
            )
        except Exception as e:
            stub = _stub_resolve_shape(
                error=f"{type(e).__name__}: {e}",
                tested_function=tested_function,
                script_path_str=str(script_path),
                snippet=callee,
            )
            rows.append(
                one_row(
                    callee_index=idx,
                    tested_function=tested_function,
                    callee=callee,
                    navigation=stub,
                )
            )

    return rows


def _default_eval_workers() -> int:
    env = os.environ.get("HOPPSCOTCH_CODE_NAV_EVAL_WORKERS")
    if env is not None:
        try:
            return max(1, int(env.strip(), 10))
        except ValueError:
            pass
    cpus = os.cpu_count() or 1
    return max(1, min(3, cpus))


def _pool_max_workers(num_items: int, workers: Optional[int]) -> int:
    if num_items <= 0:
        return 1
    if workers is None:
        return min(_default_eval_workers(), num_items)
    return max(1, min(workers, num_items))


def run_eval(
    limit: Optional[int] = None,
    ids: Optional[list[int]] = None,
    workers: Optional[int] = None,
) -> Tuple[List[dict], int, int]:
    eval_items = load_eval_set(EVAL_JSON)
    if ids is not None:
        id_set = set(ids)
        eval_items = [item for item in eval_items if item.get("id") in id_set]
    if limit is not None:
        eval_items = eval_items[:limit]

    max_workers = _pool_max_workers(len(eval_items), workers)
    if not eval_items:
        return [], max_workers, 0

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        per_sample = list(executor.map(_eval_sample, eval_items))
    flat = [row for sample_rows in per_sample for row in sample_rows]
    skipped_no_callees = sum(1 for rows in per_sample if not rows)
    return flat, max_workers, skipped_no_callees


def main():
    ap = argparse.ArgumentParser(description="Run code_navigation_TypeScript on hoppscotch.json evaluation set")
    ap.add_argument("--limit", type=int, default=None, help="Max number of items to run (default: all)")
    ap.add_argument("--ids", type=int, nargs="+", default=None, metavar="ID", help="Run only these evaluation IDs (e.g. --ids 14 79 95)")
    ap.add_argument("--output", "-o", type=str, default=None, help="Write summary output to this file as well as stdout")
    ap.add_argument(
        "--results-json",
        type=str,
        default=None,
        metavar="PATH",
        help="Write full JSON results to this path (default: hoppscotch_eval_results.json)",
    )
    ap.add_argument("--workers", type=int, default=None, help="Number of parallel workers (default: min(32, number of samples))")
    args = ap.parse_args()

    if not EVAL_JSON.exists():
        print(f"Eval file not found: {EVAL_JSON}", file=sys.stderr)
        sys.exit(1)
    if not HOPPSCOTCH_REPO_ROOT.is_dir():
        print(f"Hoppscotch repo root not found: {HOPPSCOTCH_REPO_ROOT}", file=sys.stderr)
        sys.exit(1)

    out_lines: List[str] = []

    def emit(msg: str = ""):
        print(msg)
        out_lines.append(msg)

    emit("Running code_navigation_TypeScript on hoppscotch.json evaluation set...")
    emit(f"Repo root: {HOPPSCOTCH_REPO_ROOT}")
    if args.limit:
        emit(f"Limit: first {args.limit} items")
    if args.ids:
        emit(f"Ids only: {args.ids}")
    emit()

    start_time = time.perf_counter()
    results, pool_workers, skipped_no_callees = run_eval(
        limit=args.limit, ids=args.ids, workers=args.workers
    )
    runtime_seconds = time.perf_counter() - start_time
    passed = [r for r in results if r.get("ok")]
    failed = [r for r in results if not r.get("ok")]
    sample_ids = {r["sample_id"] for r in results}
    n_samples = len(sample_ids)
    samples_all_ok = {
        sid for sid in sample_ids if all(r.get("ok") for r in results if r["sample_id"] == sid)
    }
    samples_any_fail = sample_ids - samples_all_ok

    emit("=" * 70)
    emit("SUMMARY")
    emit("=" * 70)
    emit(f"Process pool:   max_workers={pool_workers} (override: --workers or HOPPSCOTCH_CODE_NAV_EVAL_WORKERS)")
    emit(f"Runtime:        {runtime_seconds:.2f}s")
    emit(f"Samples skipped (no extractable callees): {skipped_no_callees}")
    emit(f"Samples (ids):    {n_samples}")
    emit(f"Callee rows:      {len(results)} total, {len(passed)} ok, {len(failed)} failed")
    if results:
        row_pct = 100.0 * len(passed) / len(results)
        emit(f"Row pass rate:    {row_pct:.1f}%")
    emit(
        f"Samples all ok:   {len(samples_all_ok)} / {n_samples} "
        f"(every callee row succeeded for that sample)"
    )
    emit()

    if passed:
        emit("--- OK rows (first 30) ---")
        for r in passed[:30]:
            od = (
                (r.get("definitions") or [{}])[0].get("outer_definition")
                if r.get("definitions")
                else None
            ) or {}
            chosen = od.get("repo_relative_path") or "(no path)"
            callee_preview = (r.get("callee") or "")[:60]
            if len(r.get("callee") or "") > 60:
                callee_preview += "…"
            emit(
                f"  sample={r['sample_id']} idx={r['callee_index']} fn={r.get('tested_function')} -> {chosen}"
            )
            emit(f"    callee: {callee_preview!r}")
        if len(passed) > 30:
            emit(f"  ... and {len(passed) - 30} more ok rows")
        emit()

    if failed:
        emit("--- FAILED rows ---")
        for r in failed:
            err = r.get("error") or "unknown"
            callee_preview = (r.get("callee") or "")[:72]
            emit(
                f"  sample={r['sample_id']} idx={r['callee_index']} fn={r.get('tested_function')}"
            )
            emit(f"    callee: {callee_preview!r}")
            emit(f"    error:  {err}")
            if r.get("script_path"):
                emit(f"    file:   {r['script_path']}")
        emit()

    out_json = Path(args.results_json).resolve() if args.results_json else (DOCPRISM_ROOT / "hoppscotch_eval_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(
            {
                "summary": {
                    "runtime_seconds": round(runtime_seconds, 2),
                    "samples_skipped_no_callees": skipped_no_callees,
                    "unique_sample_ids": n_samples,
                    "callee_rows_total": len(results),
                    "callee_rows_ok": len(passed),
                    "callee_rows_failed": len(failed),
                    "samples_all_rows_ok": len(samples_all_ok),
                    "samples_with_any_failed_row": len(samples_any_fail),
                },
                "results": results,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    emit(f"Full results written to: {out_json}")

    if args.output:
        out_path = Path(args.output)
        out_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        print(f"Summary written to: {out_path}", file=sys.stderr)

    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
