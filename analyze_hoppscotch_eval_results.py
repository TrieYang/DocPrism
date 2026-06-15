#!/usr/bin/env python3
"""
Analyze hoppscotch_eval_results.json for function (call-site) resolutions only.

Definition quality (heuristics):
  declaration_layer:
    - Definition file ends with .d.ts (typical IDE first hop to types).
    - OR path under node_modules and snippet has no '{' (type-only / overload line).
  implementation_like:
    - Everything else with non-empty full_def_source (repo .ts/.tsx with bodies, etc.).

  external: 'node_modules' in definition path.
  internal: otherwise (monorepo package sources).

Attribute resolutions (usage.kind == attr) are excluded.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


def _norm_path(p: str) -> str:
    return p.replace("\\", "/")


def _outer_def(row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    defs = row.get("definitions") or []
    if not defs:
        return None
    od = defs[0].get("outer_definition")
    return od if isinstance(od, dict) else None


def _def_path(od: Optional[Dict[str, Any]]) -> str:
    if not od:
        return ""
    return od.get("path") or od.get("uri") or ""


def _def_src(od: Optional[Dict[str, Any]]) -> str:
    if not od:
        return ""
    return (od.get("full_def_source") or "").strip()


def classify_definition(path: str, src: str) -> Tuple[str, str]:
    """
    Returns (bucket, detail) where bucket is 'declaration_layer' | 'implementation_like' | 'missing'.
    """
    path_n = _norm_path(path)
    if not path_n and not src:
        return "missing", "no_definition"

    if path_n.endswith(".d.ts"):
        return "declaration_layer", "d_ts_file"

    in_nm = "node_modules/" in path_n or "/node_modules/" in path_n
    if in_nm and "{" not in src:
        return "declaration_layer", "node_modules_no_body_brace"

    head = src[:800] if src else ""
    if re.search(r"^\s*export\s+declare\b", head, re.M):
        return "declaration_layer", "export_declare"

    if src and "{" not in src and src.rstrip().endswith(";"):
        if in_nm or path_n.endswith((".ts", ".tsx", ".mts", ".cts")):
            return "declaration_layer", "signature_only_no_brace"

    if not src:
        return "missing", "empty_full_def_source"

    return "implementation_like", "has_body_or_non_signature_ts"


def internal_external(path: str) -> str:
    path_n = _norm_path(path)
    if not path_n:
        return "unknown"
    if "node_modules/" in path_n:
        return "external"
    return "internal"


def pct(num: int, den: int) -> float:
    if den == 0:
        return 0.0
    return 100.0 * num / den


def _is_function_call_row(row: Dict[str, Any]) -> bool:
    return ((row.get("input") or {}).get("usage") or {}).get("kind") == "call"


def summarize_function_rows(rows: List[Dict[str, Any]], label: str, emit: Callable[[str], None]) -> None:
    total = len(rows)
    ok_rows = [r for r in rows if r.get("ok")]
    with_def: List[Tuple[Dict[str, Any], str, str, str, str]] = []
    for r in ok_rows:
        od = _outer_def(r)
        p = _def_path(od)
        s = _def_src(od)
        bucket, _detail = classify_definition(p, s)
        ie = internal_external(p)
        with_def.append((r, p, s, bucket, ie))

    decl = sum(1 for _, _, _, b, _ in with_def if b == "declaration_layer")
    impl = sum(1 for _, _, _, b, _ in with_def if b == "implementation_like")
    miss = sum(1 for _, _, _, b, _ in with_def if b == "missing")
    n = len(with_def)

    emit(f"\n=== {label} (function rows: {total}, ok: {len(ok_rows)}, with definition: {n}) ===")
    emit(
        f"  declaration_layer: {decl} ({pct(decl, n):.1f}%)  "
        f"implementation_like: {impl} ({pct(impl, n):.1f}%)  "
        f"missing/empty: {miss} ({pct(miss, n):.1f}%)"
    )

    for scope in ("internal", "external", "unknown"):
        sub = [(r, p, s, b, ie) for r, p, s, b, ie in with_def if ie == scope]
        if not sub:
            continue
        d = sum(1 for *_, b, _ in sub if b == "declaration_layer")
        i = sum(1 for *_, b, _ in sub if b == "implementation_like")
        m = sum(1 for *_, b, _ in sub if b == "missing")
        sn = len(sub)
        emit(
            f"  [{scope}] n={sn}  decl: {d} ({pct(d, sn):.1f}%)  "
            f"impl: {i} ({pct(i, sn):.1f}%)  missing: {m} ({pct(m, sn):.1f}%)"
        )


def build_stats(rows: List[Dict[str, Any]], *, ok_only: bool = True) -> Dict[str, Any]:
    """Aggregate declaration/implementation and internal/external counts."""
    pool = [r for r in rows if (r.get("ok") if ok_only else True)]
    counts: Dict[str, int] = defaultdict(int)
    cross: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    detail_counts: Dict[str, int] = defaultdict(int)
    rows_out: List[Dict[str, Any]] = []

    for r in pool:
        od = _outer_def(r)
        p = _def_path(od)
        s = _def_src(od)
        bucket, detail = classify_definition(p, s)
        ie = internal_external(p)
        counts[bucket] += 1
        counts[f"scope_{ie}"] += 1
        cross[ie][bucket] += 1
        detail_counts[detail] += 1
        rows_out.append(
            {
                "sample_id": r.get("sample_id"),
                "callee_index": r.get("callee_index"),
                "callee": (r.get("callee") or "")[:500],
                "usage_kind": ((r.get("input") or {}).get("usage") or {}).get("kind"),
                "ok": bool(r.get("ok")),
                "definition_path": _norm_path(p),
                "bucket": bucket,
                "detail": detail,
                "internal_external": ie,
            }
        )

    n = len(pool)
    pct_map = {
        k: round(pct(v, n), 2) for k, v in counts.items() if not k.startswith("scope_")
    }
    scope_n = counts.get("scope_internal", 0) + counts.get("scope_external", 0) + counts.get("scope_unknown", 0)
    scope_pct = {
        "internal": round(pct(counts.get("scope_internal", 0), scope_n), 2),
        "external": round(pct(counts.get("scope_external", 0), scope_n), 2),
        "unknown": round(pct(counts.get("scope_unknown", 0), scope_n), 2),
    }
    return {
        "rows_analyzed": n,
        "counts": dict(counts),
        "percentages": {
            "declaration_layer": pct_map.get("declaration_layer", 0.0),
            "implementation_like": pct_map.get("implementation_like", 0.0),
            "missing": pct_map.get("missing", 0.0),
            "internal": scope_pct["internal"],
            "external": scope_pct["external"],
            "unknown": scope_pct["unknown"],
        },
        "cross_tab": {ie: dict(buckets) for ie, buckets in cross.items()},
        "detail_counts": dict(detail_counts),
        "per_row": rows_out,
    }


def write_csv(path: Path, per_row: List[Dict[str, Any]]) -> None:
    import csv

    fields = [
        "sample_id",
        "callee_index",
        "usage_kind",
        "ok",
        "bucket",
        "internal_external",
        "detail",
        "definition_path",
        "callee",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in per_row:
            w.writerow(row)


def summarize_unique_functions(rows: List[Dict[str, Any]], label: str, emit: Callable[[str], None]) -> None:
    """One row per distinct callee snippet (first occurrence wins)."""
    seen: Dict[str, Tuple[str, str, str]] = {}
    order: List[str] = []
    for r in rows:
        if not r.get("ok"):
            continue
        callee = (r.get("callee") or "").strip()
        if not callee or callee in seen:
            continue
        od = _outer_def(r)
        p = _def_path(od)
        s = _def_src(od)
        b, _d = classify_definition(p, s)
        ie = internal_external(p)
        seen[callee] = (b, ie, p)
        order.append(callee)

    buckets = defaultdict(int)
    by_ie = defaultdict(lambda: defaultdict(int))
    for c in order:
        b, ie, _p = seen[c]
        buckets[b] += 1
        by_ie[ie][b] += 1

    n = len(order)
    emit(f"\n=== {label} — UNIQUE functions (n={n}) ===")
    emit(
        f"  declaration_layer: {buckets['declaration_layer']} ({pct(buckets['declaration_layer'], n):.1f}%)  "
        f"implementation_like: {buckets['implementation_like']} ({pct(buckets['implementation_like'], n):.1f}%)  "
        f"missing: {buckets['missing']} ({pct(buckets['missing'], n):.1f}%)"
    )
    for ie in ("internal", "external", "unknown"):
        subn = sum(by_ie[ie].values())
        if subn == 0:
            continue
        d = by_ie[ie]["declaration_layer"]
        i = by_ie[ie]["implementation_like"]
        m = by_ie[ie]["missing"]
        emit(
            f"  [{ie}] n={subn}  decl: {d} ({pct(d, subn):.1f}%)  "
            f"impl: {i} ({pct(i, subn):.1f}%)  missing: {m} ({pct(m, subn):.1f}%)"
        )


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Analyze hoppscotch eval results: function (call) sites only."
    )
    ap.add_argument(
        "json_path",
        nargs="?",
        default=str(Path(__file__).resolve().parent / "hoppscotch_eval_results.json"),
        help="Path to hoppscotch_eval_results.json",
    )
    ap.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Write the full report to this path (default: timestamped file next to the JSON input)",
    )
    ap.add_argument(
        "--no-save",
        action="store_true",
        help="Do not write a report file (stdout only)",
    )
    ap.add_argument(
        "--json-out",
        metavar="FILE",
        help="Write structured stats JSON (percentages, cross-tabs, per-row detail)",
    )
    ap.add_argument(
        "--csv-out",
        metavar="FILE",
        help="Write per-row CSV export",
    )
    ap.add_argument(
        "--include-attributes",
        action="store_true",
        help="Include attribute rows in addition to function call rows",
    )
    args = ap.parse_args()
    path = Path(args.json_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    all_rows: List[Dict[str, Any]] = data.get("results") or []
    if args.include_attributes:
        rows = list(all_rows)
        scope_label = "all call + attribute rows"
    else:
        rows = [r for r in all_rows if _is_function_call_row(r)]
        scope_label = "function call rows only"

    lines: List[str] = []

    def emit(msg: str) -> None:
        lines.append(msg)
        print(msg)

    emit("Hoppscotch eval — definition analysis")
    emit(f"Input: {path}")
    emit(f"  scope: {len(rows)} {scope_label} (total rows in file: {len(all_rows)})")
    summ = data.get("summary") or {}
    for k in ("callee_rows_total", "callee_rows_ok", "unique_sample_ids", "runtime_seconds"):
        if k in summ:
            emit(f"  eval summary.{k}: {summ[k]}")

    stats = build_stats(rows, ok_only=True)
    emit("\n=== SUMMARY (ok rows with definitions) ===")
    emit(f"  rows analyzed: {stats['rows_analyzed']}")
    emit(
        f"  declaration_layer: {stats['counts'].get('declaration_layer', 0)} "
        f"({stats['percentages']['declaration_layer']}%)"
    )
    emit(
        f"  implementation_like: {stats['counts'].get('implementation_like', 0)} "
        f"({stats['percentages']['implementation_like']}%)"
    )
    emit(
        f"  missing/empty: {stats['counts'].get('missing', 0)} "
        f"({stats['percentages']['missing']}%)"
    )
    emit(
        f"  internal: {stats['counts'].get('scope_internal', 0)} "
        f"({stats['percentages']['internal']}%)"
    )
    emit(
        f"  external: {stats['counts'].get('scope_external', 0)} "
        f"({stats['percentages']['external']}%)"
    )
    emit(f"  cross-tab (internal/external x bucket): {json.dumps(stats['cross_tab'], indent=2)}")

    summarize_function_rows(rows, "ALL ROWS IN SCOPE", emit)
    summarize_unique_functions(rows, "ALL ROWS IN SCOPE", emit)

    ext_decl = 0
    ext_impl = 0
    for r in rows:
        if not r.get("ok"):
            continue
        od = _outer_def(r)
        p = _def_path(od)
        s = _def_src(od)
        b, _ = classify_definition(p, s)
        if internal_external(p) != "external":
            continue
        if b == "declaration_layer":
            ext_decl += 1
        elif b == "implementation_like":
            ext_impl += 1
    ext_total = ext_decl + ext_impl
    emit("\n=== External definitions only (node_modules), functions ===")
    emit(f"  rows: {ext_total}  declaration_layer: {ext_decl} ({pct(ext_decl, ext_total):.1f}%)")
    emit(
        f"  implementation_like under node_modules: {ext_impl} ({pct(ext_impl, ext_total):.1f}%)"
    )
    emit(
        "\nInterpretation: a large share of external + declaration_layer suggests many functions"
        "\n  resolve like IDE first-hop to .d.ts or generated signatures; a second 'go to implementation'"
        "\n  step might land in .ts implementation for some packages."
    )

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    base = path.parent

    if args.json_out:
        json_path = Path(args.json_out)
    else:
        json_path = base / f"hoppscotch_eval_analysis_{ts}.json"
    json_payload = {
        "input": str(path.resolve()),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": scope_label,
        "eval_summary": summ,
        "stats": {k: v for k, v in stats.items() if k != "per_row"},
        "per_row_count": len(stats["per_row"]),
    }
    json_path.write_text(json.dumps(json_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nJSON stats written to: {json_path.resolve()}", file=sys.stderr)

    if args.csv_out:
        csv_path = Path(args.csv_out)
    else:
        csv_path = base / f"hoppscotch_eval_analysis_{ts}.csv"
    write_csv(csv_path, stats["per_row"])
    print(f"CSV rows written to: {csv_path.resolve()}", file=sys.stderr)

    if not args.no_save:
        if args.output:
            out_path = Path(args.output)
        else:
            out_path = base / f"hoppscotch_function_eval_analysis_{ts}.txt"
        body = "\n".join(lines) + "\n"
        out_path.write_text(body, encoding="utf-8")
        print(f"Report written to: {out_path.resolve()}", file=sys.stderr)


if __name__ == "__main__":
    main()
