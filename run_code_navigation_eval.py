#!/usr/bin/env python3
"""
Run code_navigation_TypeScript on every qualifying callee in each sample
from a repo's *.json evaluation set.

Supported repos (pass via --repo):
  hoppscotch, n8n, nest, puppeteer

For each sample function snippet:
  1. Extract the tested function name and all outside callees
  2. Call resolve_from_snippet for each callee
  3. Write results to <repo>_eval_results.json

Usage:
  python run_code_navigation_eval.py --repo hoppscotch
  python run_code_navigation_eval.py --repo n8n --limit 5
  python run_code_navigation_eval.py --repo nest --ids 1 2 3 -o nest_eval_output.txt
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
SUPPORTED_REPOS = ("hoppscotch", "n8n", "nest", "puppeteer")

# Absolute path prefix used inside the evaluation JSON files.
KYLE_TS_PREFIX = "/Users/kyle/Documents/ubc/research/data/ts/"


# ---------------------------------------------------------------------------
# Path / dataset helpers
# ---------------------------------------------------------------------------


def repo_paths(repo: str) -> Tuple[Path, Path, Path]:
    """Return (repo_root, eval_json, results_json) for a supported repo name."""
    if repo not in SUPPORTED_REPOS:
        raise ValueError(f"unsupported repo {repo!r}; choose from {SUPPORTED_REPOS}")
    repo_root = SCRIPT_DIR / repo
    eval_json = SCRIPT_DIR / f"{repo}.json"
    results_json = SCRIPT_DIR / f"{repo}_eval_results.json"
    return repo_root, eval_json, results_json


def load_eval_set(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def json_filename_to_local_path(filename: str, repo: str, repo_root: Path) -> Path:
    """Map absolute paths from the JSON onto the local checkout."""
    norm = filename.replace("\\", "/")
    prefix = f"{KYLE_TS_PREFIX}{repo}/"
    if norm.startswith(prefix):
        return repo_root / norm[len(prefix) :]
    marker = f"/{repo}/"
    idx = norm.find(marker)
    if idx >= 0:
        return repo_root / norm[idx + len(marker) :]
    return repo_root / Path(norm).name


# ---------------------------------------------------------------------------
# Tested-function / callee extraction
# ---------------------------------------------------------------------------


def _skip_generics(text: str, pos: int) -> int:
    """If text[pos:] starts with <...>, return index after the matching '>'. Else return pos."""
    i = pos
    while i < len(text) and text[i] in " \t":
        i += 1
    if i >= len(text) or text[i] != "<":
        return pos
    depth = 1
    i += 1
    while i < len(text):
        if text[i] == "<":
            depth += 1
        elif text[i] == ">":
            depth -= 1
            if depth == 0:
                return i + 1
        elif text[i] in "\"'":
            quote = text[i]
            i += 1
            while i < len(text) and text[i] != quote:
                i += 2 if text[i] == "\\" else 1
            i += 1
            continue
        i += 1
    return pos


_METHOD_MODIFIERS = (
    "async",
    "public",
    "protected",
    "private",
    "static",
    "abstract",
    "override",
    "readonly",
)


def extract_tested_function(code: str) -> str | None:
    """Extract the function/method/getter/setter name from a code snippet."""
    code = code.strip()
    m = re.match(r"(?:async\s+)?function\s+(\w+)\s*\(", code)
    if m:
        return m.group(1)
    # getters / setters (optionally with access modifiers)
    m = re.match(
        r"(?:(?:public|protected|private|static|abstract|override)\s+)*get\s+(\w+)\s*\(",
        code,
    )
    if m:
        return m.group(1)
    m = re.match(
        r"(?:(?:public|protected|private|static|abstract|override)\s+)*set\s+(\w+)\s*\(",
        code,
    )
    if m:
        return m.group(1)
    # Method / constructor-like: optional modifiers, then name, optional generics, then (
    mod = "|".join(_METHOD_MODIFIERS)
    m = re.match(rf"(?:(?:{mod})\s+)*(\w+)", code)
    if m:
        name = m.group(1)
        if name in _METHOD_MODIFIERS:
            return None
        rest_pos = _skip_generics(code, m.end())
        if rest_pos < len(code) and re.match(r"\s*\(", code[rest_pos:]):
            return name
        # Property getter shorthand already covered; also allow `get name():`
        if rest_pos < len(code) and re.match(r"\s*:", code[rest_pos:]):
            # e.g. `get path(): string {` already handled above; bare `name: type` is not a fn
            pass
    return None


def _find_matching_closing_paren(text: str, open_pos: int) -> int | None:
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
        elif ch in "\"'":
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
            continue
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
    """Params + names defined in the body — excluded from 'outside' callees."""
    lines = code.split("\n")
    first_line = lines[0] if lines else ""
    body = "\n".join(lines[1:]) if len(lines) > 1 else ""
    locals_set: set[str] = {tested_function}

    paren_open = first_line.find("(")
    if paren_open != -1:
        close = _find_matching_closing_paren(first_line, paren_open)
        if close is not None:
            params_str = first_line[paren_open + 1 : close]
            for part in re.split(r"[,=]", params_str):
                part = part.strip()
                if part.startswith("..."):
                    part = part[3:].strip()
                m = re.match(r"([A-Za-z_$][A-Za-z0-9_$]*)", part)
                if m:
                    locals_set.add(m.group(1))

    for m in re.finditer(r"(?:async\s+)?function\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*\(", body):
        locals_set.add(m.group(1))
    for m in re.finditer(r"\b(?:const|let|var)\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*[=:]", body):
        locals_set.add(m.group(1))
    for m in re.finditer(r"\bfor\s*\(\s*(?:const|let)\s+([A-Za-z_$][A-Za-z0-9_$]*)", body):
        locals_set.add(m.group(1))

    locals_set.update(_extract_arrow_callback_param_names(body))
    return locals_set


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
        "async",
        "function",
        "await",
        "yield",
        "throw",
        "import",
        "super",
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
    paren_depth = bracket_depth = brace_depth = 0
    while i >= 0:
        ch = body[i]
        if ch == ")":
            paren_depth += 1
        elif ch == "(":
            if paren_depth > 0:
                paren_depth -= 1
            elif bracket_depth == 0 and brace_depth == 0:
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
    Extract callees from the function body that are 'outside':
      1) Calls whose root name is not local
      2) Attribute access whose receiver is not local
    """
    lines = code.split("\n")
    body = "\n".join(lines[1:]) if len(lines) > 1 else code
    local_names = _extract_local_names(code, tested_function)
    seen: set[str] = set()

    def is_outside_root(name: str) -> bool:
        return name not in local_names and name != tested_function

    result: list[str] = []

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
        callee = body[start : close + 1].strip()
        if callee in seen:
            continue
        seen.add(callee)
        result.append(callee)

    call_re = re.compile(r"\b([A-Za-z_$][A-Za-z0-9_$]*)\s*\(")
    for m in call_re.finditer(body):
        if _is_inside_string_literal(body, m.start(0)):
            continue
        if m.start(0) > 0 and body[m.start(0) - 1] == ".":
            continue
        line_start = body.rfind("\n", 0, m.start(0)) + 1
        nl = body.find("\n", m.start(0))
        line = body[line_start : nl if nl != -1 else len(body)]
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
        callee = body[m.start(0) : close + 1].strip()
        if callee in seen:
            continue
        seen.add(callee)
        result.append(callee)

    attr_re = re.compile(r"([A-Za-z_$][A-Za-z0-9_$]*)\s*\.\s*([A-Za-z_$][A-Za-z0-9_$]*)")
    for m in attr_re.finditer(body):
        if _is_inside_string_literal(body, m.start(0)):
            continue
        line_start = body.rfind("\n", 0, m.start(0)) + 1
        nl = body.find("\n", m.start(0))
        line = body[line_start : nl if nl != -1 else len(body)]
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
        if any(s.startswith(full + "(") for s in seen):
            continue
        seen.add(full)
        result.append(full)

    return result


# ---------------------------------------------------------------------------
# Per-sample evaluation (top-level for ProcessPoolExecutor)
# ---------------------------------------------------------------------------

# Set by the main process before spawning workers (passed via initializer).
_WORKER_REPO: str = ""
_WORKER_REPO_ROOT: Path = Path()


def _init_worker(repo: str, repo_root: str) -> None:
    global _WORKER_REPO, _WORKER_REPO_ROOT
    _WORKER_REPO = repo
    _WORKER_REPO_ROOT = Path(repo_root)
    sys.path.insert(0, str(SCRIPT_DIR))


def _stub_resolve_shape(
    *,
    error: str,
    tested_function: str = "",
    script_path_str: str = "",
    snippet: str = "",
) -> Dict[str, Any]:
    return {
        "ok": False,
        "input": {
            "repo_root": str(_WORKER_REPO_ROOT),
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


def _collect_jobs(
    eval_items: list[dict],
    repo: str,
    repo_root: Path,
) -> Tuple[List[dict], int]:
    """
    Build resolve jobs from samples, deduping by callee text globally.

    First occurrence of each callee string wins (any sample). Later duplicates
    are skipped and never resolved again.
    Returns ``(jobs, skipped_no_callees)``.
    """
    jobs: List[dict] = []
    seen_callees: set[str] = set()
    skipped_no_callees = 0

    for item in eval_items:
        eid = item.get("id", "?")
        filename = item.get("filename", "")
        code = item.get("code", "")
        script_path = json_filename_to_local_path(filename, repo, repo_root)

        if not code:
            jobs.append(
                {
                    "sample_id": eid,
                    "callee_index": 0,
                    "tested_function": None,
                    "script_path": str(script_path),
                    "callee": None,
                    "error": "missing code",
                }
            )
            continue

        tested_function = extract_tested_function(code)
        if not tested_function:
            jobs.append(
                {
                    "sample_id": eid,
                    "callee_index": 0,
                    "tested_function": None,
                    "script_path": str(script_path),
                    "callee": None,
                    "error": "could not extract tested_function",
                }
            )
            continue

        callees = extract_all_callees(code, tested_function)
        if not callees:
            skipped_no_callees += 1
            continue

        if not script_path.exists():
            # Still only enqueue the first not-yet-seen callee for this miss.
            for idx, callee in enumerate(callees):
                if callee in seen_callees:
                    continue
                seen_callees.add(callee)
                jobs.append(
                    {
                        "sample_id": eid,
                        "callee_index": idx,
                        "tested_function": tested_function,
                        "script_path": str(script_path),
                        "callee": callee,
                        "error": f"file not found: {script_path}",
                    }
                )
                break
            continue

        for idx, callee in enumerate(callees):
            if callee in seen_callees:
                continue
            seen_callees.add(callee)
            jobs.append(
                {
                    "sample_id": eid,
                    "callee_index": idx,
                    "tested_function": tested_function,
                    "script_path": str(script_path),
                    "callee": callee,
                    "error": None,
                }
            )

    return jobs, skipped_no_callees


def _eval_job(job: dict) -> dict:
    """Resolve one (already-deduped) callee job. Top-level for ProcessPoolExecutor."""
    from code_navigation_TypeScript import resolve_from_snippet

    eid = job["sample_id"]
    callee_index = job["callee_index"]
    tested_function = job.get("tested_function")
    script_path = Path(job["script_path"]) if job.get("script_path") else None
    callee = job.get("callee")
    pre_error = job.get("error")

    def one_row(navigation: Dict[str, Any]) -> dict:
        return {
            "sample_id": eid,
            "callee_index": callee_index,
            "tested_function": tested_function,
            "script_path": str(script_path) if script_path else None,
            "callee": callee,
            **navigation,
        }

    if pre_error:
        return one_row(
            _stub_resolve_shape(
                error=pre_error,
                tested_function=tested_function or "",
                script_path_str=str(script_path) if script_path else "",
                snippet=callee or "",
            )
        )

    assert script_path is not None and tested_function and callee
    try:
        res = resolve_from_snippet(
            repo_root=_WORKER_REPO_ROOT,
            script_path=script_path,
            tested_function=tested_function,
            snippet=callee,
            anchor=callee,
        )
        return one_row(res)
    except Exception as e:
        return one_row(
            _stub_resolve_shape(
                error=f"{type(e).__name__}: {e}",
                tested_function=tested_function,
                script_path_str=str(script_path),
                snippet=callee,
            )
        )


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def _default_eval_workers() -> int:
    env = os.environ.get("CODE_NAV_EVAL_WORKERS")
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
    repo: str,
    *,
    limit: Optional[int] = None,
    ids: Optional[list[int]] = None,
    workers: Optional[int] = None,
) -> Tuple[List[dict], int, int, int, int, Path]:
    """
    Returns
    ``(results, max_workers, skipped_no_callees, jobs_before_dedupe, skipped_dup_callees, results_json)``.
    """
    repo_root, eval_json, results_json = repo_paths(repo)
    eval_items = load_eval_set(eval_json)
    if ids is not None:
        id_set = set(ids)
        eval_items = [item for item in eval_items if item.get("id") in id_set]
    if limit is not None:
        eval_items = eval_items[:limit]

    # Count raw callee occurrences before dedupe (for summary).
    raw_callee_count = 0
    for item in eval_items:
        code = item.get("code") or ""
        fn = extract_tested_function(code) if code else None
        if fn:
            raw_callee_count += len(extract_all_callees(code, fn))

    jobs, skipped_no_callees = _collect_jobs(eval_items, repo, repo_root)
    # Jobs that are real callees (have callee text); error-only rows without callee
    # don't count toward dedupe savings.
    unique_callee_jobs = sum(1 for j in jobs if j.get("callee"))
    skipped_dup_callees = max(0, raw_callee_count - unique_callee_jobs)

    max_workers = _pool_max_workers(len(jobs), workers)
    if not jobs:
        return [], max_workers, skipped_no_callees, raw_callee_count, skipped_dup_callees, results_json

    with ProcessPoolExecutor(
        max_workers=max_workers,
        initializer=_init_worker,
        initargs=(repo, str(repo_root.resolve())),
    ) as executor:
        results = []
        total = len(jobs)
        for i, row in enumerate(executor.map(_eval_job, jobs), start=1):
            results.append(row)
            if i == 1 or i % 25 == 0 or i == total:
                print(f"  progress: {i}/{total} jobs", flush=True)
    return (
        results,
        max_workers,
        skipped_no_callees,
        raw_callee_count,
        skipped_dup_callees,
        results_json,
    )


def _classify_resolution_path(row: dict) -> str:
    """Bucket a result into source_definition / definition_or_implementation / heuristics / failed."""
    path = row.get("resolution_path")
    if path in (
        "source_definition",
        "definition_or_implementation",
        "heuristics",
        "failed",
    ):
        return path
    if not row.get("ok"):
        return "failed"
    reason = row.get("chosen_definition_reason") or {}
    note = str(reason.get("note") or "")
    if "go_to_source_definition_primary" in note:
        return "source_definition"
    if (
        reason.get("type_or_signature_surface")
        or "type_or_signature" in note
        or "external_runtime" in note
        or "post_upgrade" in note
        or "runtime_unresolved" in note
        or "definition_via_imports" in note
    ):
        return "heuristics"
    return "definition_or_implementation"


def _resolution_path_stats(results: List[dict]) -> Dict[str, Any]:
    from collections import Counter

    counts = Counter(_classify_resolution_path(r) for r in results)
    total = len(results) or 1
    ok_total = sum(1 for r in results if r.get("ok")) or 1
    labels = (
        ("source_definition", "goToSourceDefinition"),
        ("definition_or_implementation", "definition/implementation"),
        ("heuristics", "heuristics"),
        ("failed", "failed (no path / error)"),
    )
    breakdown = {}
    for key, label in labels:
        n = counts.get(key, 0)
        breakdown[key] = {
            "label": label,
            "count": n,
            "pct_of_all_rows": round(100.0 * n / total, 1),
            "pct_of_ok_rows": (
                round(100.0 * n / ok_total, 1) if key != "failed" else None
            ),
        }
    return {"counts": dict(counts), "breakdown": breakdown}


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Run code_navigation_TypeScript on a repo evaluation JSON set"
    )
    ap.add_argument(
        "--repo",
        required=True,
        choices=SUPPORTED_REPOS,
        help="Which evaluation set / local checkout to run against",
    )
    ap.add_argument("--limit", type=int, default=None, help="Max number of samples to run")
    ap.add_argument(
        "--ids",
        type=int,
        nargs="+",
        default=None,
        metavar="ID",
        help="Run only these sample IDs",
    )
    ap.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Also write the human-readable summary to this file",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Parallel workers (default: min(3, CPU); override with CODE_NAV_EVAL_WORKERS)",
    )
    args = ap.parse_args()

    repo_root, eval_json, results_json = repo_paths(args.repo)
    if not eval_json.exists():
        print(f"Eval file not found: {eval_json}", file=sys.stderr)
        sys.exit(1)
    if not repo_root.is_dir():
        print(f"Repo root not found: {repo_root}", file=sys.stderr)
        sys.exit(1)

    out_lines: List[str] = []

    def emit(msg: str = "") -> None:
        print(msg, flush=True)
        out_lines.append(msg)

    emit(f"Running code_navigation_TypeScript on {args.repo}.json ...")
    emit(f"Repo root: {repo_root}")
    if args.limit:
        emit(f"Limit: first {args.limit} samples")
    if args.ids:
        emit(f"Ids only: {args.ids}")
    emit()

    start_time = time.perf_counter()
    (
        results,
        pool_workers,
        skipped_no_callees,
        raw_callee_count,
        skipped_dup_callees,
        results_json,
    ) = run_eval(args.repo, limit=args.limit, ids=args.ids, workers=args.workers)
    runtime_seconds = time.perf_counter() - start_time
    passed = [r for r in results if r.get("ok")]
    failed = [r for r in results if not r.get("ok")]
    sample_ids = {r["sample_id"] for r in results}
    n_samples = len(sample_ids)
    samples_all_ok = {
        sid for sid in sample_ids if all(r.get("ok") for r in results if r["sample_id"] == sid)
    }
    samples_any_fail = sample_ids - samples_all_ok
    path_stats = _resolution_path_stats(results)

    emit("=" * 70)
    emit("SUMMARY")
    emit("=" * 70)
    emit(f"Repo:           {args.repo}")
    emit(f"Process pool:   max_workers={pool_workers}")
    emit(f"Runtime:        {runtime_seconds:.2f}s")
    emit(f"Samples skipped (no extractable callees): {skipped_no_callees}")
    emit(f"Callees extracted (raw): {raw_callee_count}")
    emit(f"Callees skipped (duplicate text): {skipped_dup_callees}")
    emit(f"Samples (ids with rows): {n_samples}")
    emit(f"Callee rows:      {len(results)} total, {len(passed)} ok, {len(failed)} failed")
    if results:
        emit(f"Row pass rate:    {100.0 * len(passed) / len(results):.1f}%")
    emit(
        f"Samples all ok:   {len(samples_all_ok)} / {n_samples} "
        f"(every callee row succeeded for that sample)"
    )
    emit()
    emit("--- Resolution path breakdown (phase 3) ---")
    for key in (
        "source_definition",
        "definition_or_implementation",
        "heuristics",
        "failed",
    ):
        info = path_stats["breakdown"][key]
        extra = ""
        if info["pct_of_ok_rows"] is not None and key != "failed":
            extra = f", {info['pct_of_ok_rows']}% of ok"
        emit(
            f"  {info['label']}: {info['count']} "
            f"({info['pct_of_all_rows']}% of all rows{extra})"
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
            path = _classify_resolution_path(r)
            emit(
                f"  sample={r['sample_id']} idx={r['callee_index']} "
                f"fn={r.get('tested_function')} [{path}] -> {chosen}"
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
                f"  sample={r['sample_id']} idx={r['callee_index']} "
                f"fn={r.get('tested_function')}"
            )
            emit(f"    callee: {callee_preview!r}")
            emit(f"    error:  {err}")
            if r.get("script_path"):
                emit(f"    file:   {r['script_path']}")
        emit()

    with open(results_json, "w", encoding="utf-8") as f:
        json.dump(
            {
                "repo": args.repo,
                "summary": {
                    "runtime_seconds": round(runtime_seconds, 2),
                    "samples_skipped_no_callees": skipped_no_callees,
                    "callees_extracted_raw": raw_callee_count,
                    "callees_skipped_duplicate": skipped_dup_callees,
                    "unique_sample_ids": n_samples,
                    "callee_rows_total": len(results),
                    "callee_rows_ok": len(passed),
                    "callee_rows_failed": len(failed),
                    "samples_all_rows_ok": len(samples_all_ok),
                    "samples_with_any_failed_row": len(samples_any_fail),
                    "resolution_paths": path_stats,
                },
                "results": results,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    emit(f"Full results written to: {results_json}")

    if args.output:
        out_path = Path(args.output)
        out_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        print(f"Summary written to: {out_path}", file=sys.stderr)

    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
