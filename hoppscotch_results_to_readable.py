#!/usr/bin/env python3
"""Turn hoppscotch eval JSON into a readable markdown report."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _first_outer_def(row: Dict[str, Any]) -> Dict[str, Any]:
    defs = row.get("definitions") or []
    if not defs:
        return {}
    return (defs[0] or {}).get("outer_definition") or {}


def _resolution_fingerprint(row: Dict[str, Any]) -> str:
    """Hash the resolved definition payload so identical targets collapse together."""
    if not row.get("ok"):
        return f"failed:{row.get('sample_id')}:{row.get('callee_index')}:{row.get('error')}"

    od = _first_outer_def(row)
    rt = od.get("runtime_implementation") or {}
    export_surface = rt.get("export_surface") or {}
    parts = [
        od.get("path") or "",
        od.get("full_def_source") or "",
        export_surface.get("full_def_source") or "",
        rt.get("full_def_source") or "",
    ]
    return hashlib.sha256("\n---\n".join(parts).encode()).hexdigest()


def _normalize_callee_label(callee: str) -> str:
    """Collapse literal call arguments so ``E.left(x)`` groups with ``E.left(...)``."""
    callee = (callee or "").strip()
    if "(" not in callee:
        return callee
    head, _rest = callee.split("(", 1)
    return f"{head.strip()}(...)"


def _dedupe_results_by_resolution(
    results: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """
    Keep the first row for each unique resolution fingerprint.
    Attach ``_dedupe_sibling_count`` on kept rows (number of later duplicates).
    """
    seen: Dict[str, Dict[str, Any]] = {}
    order: List[str] = []
    duplicate_counts: Dict[str, int] = {}

    for row in results:
        key = _resolution_fingerprint(row)
        if key not in seen:
            seen[key] = row
            order.append(key)
            duplicate_counts[key] = 0
        else:
            duplicate_counts[key] += 1

    deduped: List[Dict[str, Any]] = []
    for key in order:
        row = dict(seen[key])
        row["_dedupe_sibling_count"] = duplicate_counts[key]
        deduped.append(row)
    return deduped, duplicate_counts


def _group_rows_by_callee(
    rows: List[Dict[str, Any]],
) -> List[Tuple[str, List[Dict[str, Any]]]]:
    """Group resolution-deduped rows by normalized callee label."""
    buckets: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    order: List[str] = []
    for row in rows:
        label = _normalize_callee_label(row.get("callee") or "")
        if label not in buckets:
            order.append(label)
        buckets[label].append(row)
    return [(label, buckets[label]) for label in order]


def _definition_content_key(row: Dict[str, Any]) -> str:
    """Fingerprint definition payload only (ignore which file hosts an identical snippet)."""
    if not row.get("ok"):
        return f"failed:{row.get('error')}"
    od = _first_outer_def(row)
    rt = od.get("runtime_implementation") or {}
    export_surface = rt.get("export_surface") or {}
    parts = [
        od.get("full_def_source") or "",
        export_surface.get("full_def_source") or "",
        rt.get("full_def_source") or "",
    ]
    return hashlib.sha256("\n---\n".join(parts).encode()).hexdigest()


def _rel_path(row: Dict[str, Any]) -> str:
    od = _first_outer_def(row)
    return od.get("repo_relative_path") or od.get("path") or "?"


def _format_call_site_brief(row: Dict[str, Any]) -> str:
    sid = row.get("sample_id")
    ci = row.get("callee_index")
    fn = row.get("tested_function") or "?"
    return f"sample {sid} · #{ci} · `{fn}`"


def _format_definition_block(row: Dict[str, Any]) -> List[str]:
    lines: List[str] = []
    od = _first_outer_def(row)
    if not od:
        return lines
    rel = od.get("repo_relative_path") or od.get("path") or "?"
    lines.append(f"- **Path:** `{rel}`")
    rng = od.get("range") or {}
    start = rng.get("start") or {}
    lines.append(
        f"- **Range:** line {start.get('line0', '?')}, col {start.get('col0', '?')}"
    )
    reason = row.get("chosen_definition_reason")
    if reason:
        lines.append(f"- **Selection:** `{reason.get('note') or reason}`")
    src = od.get("full_def_source")
    if src:
        lines.append("")
        lines.append("```typescript")
        lines.append(src.rstrip())
        lines.append("```")
    runtime = od.get("runtime_implementation") or {}
    rt_src = runtime.get("full_def_source")
    export_surface = runtime.get("export_surface") or {}
    export_src = export_surface.get("full_def_source")
    body_src = rt_src
    if export_src and rt_src and export_src.strip() in rt_src:
        body_src = rt_src.split(export_src.strip(), 1)[-1].strip()
    if export_src or rt_src:
        lines.append("")
        lines.append("**Runtime implementation**")
        lines.append("")
        if export_src:
            export_rel = (
                export_surface.get("repo_relative_path")
                or export_surface.get("path")
                or "?"
            )
            lines.append(f"- **Export surface:** `{export_rel}`")
            lines.append("")
            lines.append("```typescript")
            lines.append(export_src.rstrip())
            lines.append("```")
        if body_src and (not export_src or body_src.strip() != export_src.strip()):
            if export_src:
                lines.append("")
            rt_rel = runtime.get("repo_relative_path") or runtime.get("path") or "?"
            lines.append(f"- **Body:** `{rt_rel}`")
            lines.append("")
            lines.append("```typescript")
            lines.append(body_src.rstrip())
            lines.append("```")
        elif rt_src and not export_src:
            rt_rel = runtime.get("repo_relative_path") or runtime.get("path") or "?"
            lines.append(f"- **Path:** `{rt_rel}`")
            lines.append("")
            lines.append("```typescript")
            lines.append(rt_src.rstrip())
            lines.append("```")
    return lines


def _format_callee_group(idx: int, callee_label: str, rows: List[Dict[str, Any]]) -> List[str]:
    lines: List[str] = []
    total_siblings = sum(int(r.get("_dedupe_sibling_count") or 0) for r in rows)
    eval_rows = sum(1 + int(r.get("_dedupe_sibling_count") or 0) for r in rows)
    failed = [r for r in rows if not r.get("ok")]

    pattern_buckets: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    pattern_order: List[str] = []
    for row in rows:
        key = _definition_content_key(row)
        if key not in pattern_buckets:
            pattern_order.append(key)
        pattern_buckets[key].append(row)

    lines.append(f"## {idx}. `{callee_label}`")
    lines.append("")
    lines.append(f"- **Definition patterns:** {len(pattern_order)}")
    lines.append(f"- **Distinct resolution targets:** {len(rows)}")
    lines.append(f"- **Eval callee rows represented:** {eval_rows}")
    if total_siblings:
        lines.append(
            f"- **Collapsed duplicate resolutions:** {total_siblings} "
            f"(identical definition payload across samples)"
        )
    if failed:
        lines.append(f"- **Failed rows in group:** {len(failed)}")
    else:
        lines.append("- **Status:** OK")
    lines.append("")

    for pidx, key in enumerate(pattern_order, 1):
        group_rows = pattern_buckets[key]
        rep = group_rows[0]
        lines.append(f"### Resolution {pidx}")
        lines.append("")
        if len(group_rows) > 1:
            paths = sorted({_rel_path(r) for r in group_rows})
            lines.append(
                f"- **Same definition in {len(group_rows)} places** "
                f"({sum(1 + int(r.get('_dedupe_sibling_count') or 0) for r in group_rows)} eval rows)"
            )
            if len(paths) <= 6:
                lines.append("- **Paths:**")
                for p in paths:
                    lines.append(f"  - `{p}`")
            else:
                lines.append(f"- **Paths ({len(paths)}):**")
                for p in paths[:4]:
                    lines.append(f"  - `{p}`")
                lines.append(f"  - … and {len(paths) - 4} more")
            sites = [_format_call_site_brief(r) for r in group_rows[:6]]
            lines.append(f"- **Example call sites:** {', '.join(sites)}")
            if len(group_rows) > 6:
                lines.append(f"- **… and {len(group_rows) - 6} more call-site variants**")
            lines.append("")
        else:
            rep_ref = (rep.get("matches") or {}).get("chosen") or {}
            ref = rep_ref.get("ref") or {}
            lines.append(f"- **Function:** `{rep.get('tested_function') or '?'}`")
            lines.append(f"- **File:** `{rep.get('script_path') or '?'}`")
            if ref:
                lines.append(
                    f"- **Usage:** line {ref.get('line1', '?')}, col {ref.get('col1', '?')}"
                )
            sibling_count = int(rep.get("_dedupe_sibling_count") or 0)
            if sibling_count:
                lines.append(
                    f"- **Also seen in:** {sibling_count} other eval row"
                    f"{'s' if sibling_count != 1 else ''} with this definition"
                )
            lines.append("")

        if not rep.get("ok"):
            lines.append(f"- **Error:** {rep.get('error')}")
            lines.append("")
            continue

        lines.extend(_format_definition_block(rep))
        lines.append("")

    lines.append("---")
    lines.append("")
    return lines


def _format_row(idx: int, row: Dict[str, Any]) -> List[str]:
    lines: List[str] = []
    sid = row.get("sample_id")
    ci = row.get("callee_index")
    fn = row.get("tested_function") or "?"
    callee = row.get("callee") or ""
    script = row.get("script_path") or ""
    ok = row.get("ok", False)
    err = row.get("error")

    lines.append(f"## {idx}. Sample {sid} · callee #{ci}")
    lines.append("")
    lines.append(f"- **Function:** `{fn}`")
    lines.append(f"- **File:** `{script}`")
    lines.append(f"- **Callee:** `{callee}`")
    lines.append(f"- **Status:** {'OK' if ok else 'FAILED'}")
    sibling_count = int(row.get("_dedupe_sibling_count") or 0)
    if sibling_count:
        lines.append(
            f"- **Also seen in:** {sibling_count} other callee row"
            f"{'s' if sibling_count != 1 else ''} with the same resolved definition"
        )
    if err:
        lines.append(f"- **Error:** {err}")
    lines.append("")

    chosen = row.get("matches", {}).get("chosen")
    if chosen:
        ref = chosen.get("ref") or {}
        lines.append("### Usage site (matched in test file)")
        lines.append("")
        lines.append(
            f"Line {ref.get('line1', '?')}, col {ref.get('col1', '?')} "
            f"— pattern `{((chosen.get('meta') or {}).get('pattern'))}`"
        )
        expr = chosen.get("expr_src")
        if expr:
            lines.append("")
            lines.append("```typescript")
            lines.append(expr.strip())
            lines.append("```")
        lines.append("")

    od = _first_outer_def(row)
    if od:
        lines.append("### Resolved definition")
        lines.append("")
        rel = od.get("repo_relative_path") or od.get("path") or "?"
        lines.append(f"- **Path:** `{rel}`")
        rng = od.get("range") or {}
        start = rng.get("start") or {}
        lines.append(
            f"- **Range:** line {start.get('line0', '?')}, col {start.get('col0', '?')}"
        )
        reason = row.get("chosen_definition_reason")
        if reason:
            lines.append(f"- **Selection:** `{reason.get('note') or reason}`")
        src = od.get("full_def_source")
        if src:
            lines.append("")
            lines.append("```typescript")
            lines.append(src.rstrip())
            lines.append("```")
        runtime = od.get("runtime_implementation") or {}
        rt_src = runtime.get("full_def_source")
        export_surface = runtime.get("export_surface") or {}
        export_src = export_surface.get("full_def_source")
        body_src = rt_src
        if export_src and rt_src and export_src.strip() in rt_src:
            body_src = rt_src.split(export_src.strip(), 1)[-1].strip()
        if export_src or rt_src:
            lines.append("")
            lines.append("### Runtime implementation")
            lines.append("")
            if export_src:
                export_rel = export_surface.get("repo_relative_path") or export_surface.get("path") or "?"
                lines.append(f"- **Export surface:** `{export_rel}`")
                lines.append("")
                lines.append("```typescript")
                lines.append(export_src.rstrip())
                lines.append("```")
            if body_src and (not export_src or body_src.strip() != export_src.strip()):
                if export_src:
                    lines.append("")
                rt_rel = runtime.get("repo_relative_path") or runtime.get("path") or "?"
                lines.append(f"- **Body:** `{rt_rel}`")
                rt_rng = runtime.get("range") or {}
                rt_start = rt_rng.get("start") or {}
                lines.append(
                    f"- **Range:** line {rt_start.get('line0', '?')}, col {rt_start.get('col0', '?')}"
                )
                lines.append("")
                lines.append("```typescript")
                lines.append(body_src.rstrip())
                lines.append("```")
            elif rt_src and not export_src:
                rt_rel = runtime.get("repo_relative_path") or runtime.get("path") or "?"
                lines.append(f"- **Path:** `{rt_rel}`")
                rt_rng = runtime.get("range") or {}
                rt_start = rt_rng.get("start") or {}
                lines.append(
                    f"- **Range:** line {rt_start.get('line0', '?')}, col {rt_start.get('col0', '?')}"
                )
                lines.append("")
                lines.append("```typescript")
                lines.append(rt_src.rstrip())
                lines.append("```")
        lines.append("")

    nested = []
    defs0 = (row.get("definitions") or [{}])[0] or {}
    for u in defs0.get("argument_usages_resolved") or []:
        if u.get("ok") and u.get("definition"):
            nested.append(u)
    if nested:
        lines.append("### Nested usages resolved")
        lines.append("")
        for u in nested[:8]:
            usage = u.get("usage") or {}
            d = u.get("definition") or {}
            lines.append(
                f"- `{usage.get('name')}` → `{d.get('repo_relative_path') or d.get('path')}`"
            )
        if len(nested) > 8:
            lines.append(f"- … and {len(nested) - 8} more")
        lines.append("")

    lines.append("---")
    lines.append("")
    return lines


def json_to_markdown(
    data: Dict[str, Any],
    *,
    dedupe: bool = True,
    group_callees: bool = False,
) -> str:
    summary = data.get("summary") or {}
    results: List[Dict[str, Any]] = data.get("results") or []
    total_rows = len(results)

    if dedupe:
        results, _ = _dedupe_results_by_resolution(results)

    callee_groups = _group_rows_by_callee(results) if group_callees else []

    out: List[str] = [
        "# Hoppscotch code navigation results",
        "",
        "Generated from `code_navigation_TypeScript.resolve_from_snippet` "
        "on samples in `hoppscotch.json`.",
        "",
        "## Summary",
        "",
        f"- Runtime: {summary.get('runtime_seconds', '?')}s",
        f"- Samples with at least one callee: {summary.get('unique_sample_ids', '?')}",
        f"- Callee rows evaluated: {summary.get('callee_rows_total', total_rows)} "
        f"({summary.get('callee_rows_ok', '?')} ok, "
        f"{summary.get('callee_rows_failed', '?')} failed)",
        f"- Samples skipped (no extractable callees): "
        f"{summary.get('samples_skipped_no_callees', '?')}",
    ]
    if group_callees:
        out.append(f"- Unique callee groups shown below: {len(callee_groups)}")
    elif dedupe and len(results) != total_rows:
        out.append(
            f"- Unique resolved definitions shown below: {len(results)} "
            f"(deduped from {total_rows} callee rows)"
        )
    out.extend(["", "---", ""])

    if group_callees:
        for i, (label, group_rows) in enumerate(callee_groups, 1):
            out.extend(_format_callee_group(i, label, group_rows))
    else:
        for i, row in enumerate(results, 1):
            out.extend(_format_row(i, row))

    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--json",
        type=Path,
        default=Path("hoppscotch_navigation_results.json"),
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=Path("hoppscotch_navigation_results.md"),
    )
    ap.add_argument(
        "--no-dedupe",
        action="store_true",
        help="Include every callee row even when the resolved definition is identical",
    )
    ap.add_argument(
        "--group-callees",
        action="store_true",
        help="Group sections by callee expression instead of sample · callee #N",
    )
    args = ap.parse_args()
    data = json.loads(args.json.read_text(encoding="utf-8"))
    args.out.write_text(
        json_to_markdown(
            data,
            dedupe=not args.no_dedupe,
            group_callees=args.group_callees,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
