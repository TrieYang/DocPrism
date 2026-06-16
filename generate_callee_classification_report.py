#!/usr/bin/env python3
"""Generate callee classification markdown from navigation eval JSON."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List


def od(row: Dict[str, Any]) -> Dict[str, Any]:
    return ((row.get("definitions") or [{}])[0]).get("outer_definition") or {}


def norm(p: str) -> str:
    return (p or "").replace("\\", "/")


def path_of(row: Dict[str, Any]) -> str:
    o = od(row)
    return norm(o.get("path") or o.get("repo_relative_path") or "")


def src_of(row: Dict[str, Any]) -> str:
    return (od(row).get("full_def_source") or "").strip()


def usage_kind(row: Dict[str, Any]) -> str | None:
    return ((row.get("input") or {}).get("usage") or {}).get("kind")


def is_external(row: Dict[str, Any]) -> bool:
    return "node_modules/" in path_of(row)


def has_runtime(row: Dict[str, Any]) -> bool:
    rt = od(row).get("runtime_implementation") or {}
    return bool((rt.get("full_def_source") or "").strip())


def is_declaration_only(row: Dict[str, Any]) -> bool:
    if has_runtime(row):
        return False
    p = path_of(row)
    if p.endswith((".d.ts", ".d.cts", ".d.mts")):
        return True
    s = src_of(row)
    if "{" not in s and s.rstrip().endswith(";"):
        return True
    if re.search(r"^\s*export\s+declare\b", s[:800], re.M):
        return True
    return False


def is_const_enum_member(row: Dict[str, Any]) -> bool:
    if usage_kind(row) != "attr":
        return False
    callee = (row.get("callee") or "").strip()
    s = src_of(row)
    if re.match(r"^[A-Z][A-Z0-9_]*\.[A-Z][A-Z0-9_]*$", callee):
        return True
    if re.match(r"^this\.[A-Z][A-Z0-9_]+$", callee) and re.search(r"=\s*[^;]+;", s):
        return True
    return False


def is_prisma(row: Dict[str, Any]) -> bool:
    return ".prisma/client" in path_of(row)


def is_lib_es5(row: Dict[str, Any]) -> bool:
    return "lib.es5.d.ts" in path_of(row)


def has_interface(row: Dict[str, Any]) -> bool:
    o = od(row)
    if o.get("declaration_surface"):
        return True
    p, s = path_of(row), src_of(row)
    if p.endswith((".d.ts", ".d.cts", ".d.mts")):
        return True
    if re.search(r"^\s*export\s+declare\b", s[:800], re.M):
        return True
    if re.search(r":\s*[A-Za-z_][\w.<>,\s\[\]|&]*[;,]", s) and "{" not in s:
        return True
    if has_runtime(row):
        rt = o.get("runtime_implementation") or {}
        es = (rt.get("export_surface") or {}).get("full_def_source") or ""
        if es and (p.endswith((".d.ts", ".d.cts", ".d.mts")) or "declare" in es[:200]):
            return True
    return False


def runtime_mechanism(row: Dict[str, Any]) -> str:
    if is_declaration_only(row):
        return "declaration_only"
    if has_runtime(row):
        p = path_of(row)
        if p.endswith((".d.ts", ".d.cts", ".d.mts")) or "node_modules/" in p:
            return "dts_upgraded"
    if "{" in src_of(row):
        return "direct_impl"
    return "other"


def pct(num: int, den: int) -> float:
    return 100.0 * num / den if den else 0.0


def analyze(pool: List[Dict[str, Any]]) -> Dict[str, Any]:
    n = len(pool)
    ext = sum(1 for r in pool if is_external(r))
    decl = sum(1 for r in pool if is_declaration_only(r))
    runtime = n - decl
    int_n = n - ext
    int_decl = sum(1 for r in pool if not is_external(r) and is_declaration_only(r))
    int_rt = int_n - int_decl
    ext_decl = sum(1 for r in pool if is_external(r) and is_declaration_only(r))
    ext_rt = ext - ext_decl
    mech = Counter(runtime_mechanism(r) for r in pool if not is_declaration_only(r))
    return {
        "n": n,
        "ext": ext,
        "decl": decl,
        "runtime": runtime,
        "int_n": int_n,
        "int_decl": int_decl,
        "int_rt": int_rt,
        "ext_n": ext,
        "ext_decl": ext_decl,
        "ext_rt": ext_rt,
        "mech": mech,
    }


def iface_stats(pool: List[Dict[str, Any]]) -> Dict[str, tuple[int, int]]:
    out: Dict[str, tuple[int, int]] = {}
    for key, pred in [
        ("internal", lambda r: not is_external(r)),
        ("external", lambda r: is_external(r)),
        ("all", lambda r: True),
    ]:
        sub = [r for r in pool if pred(r)]
        out[key] = (sum(1 for r in sub if has_interface(r)), len(sub))
    return out


def generate_report(
    data: Dict[str, Any],
    *,
    commit: str = "",
    title: str = "Eval",
) -> str:
    all_rows: List[Dict[str, Any]] = data.get("results") or []
    ok = [r for r in all_rows if r.get("ok")]
    failed = [r for r in all_rows if not r.get("ok")]
    summ = data.get("summary") or {}

    no_const = [r for r in ok if not is_const_enum_member(r)]
    excl = [r for r in no_const if not is_prisma(r) and not is_lib_es5(r)]
    s1, s2 = analyze(excl), analyze(no_const)
    i1, i2 = iface_stats(excl), iface_stats(no_const)
    prisma_rows = [r for r in no_const if is_prisma(r)]
    lib_rows = [r for r in no_const if is_lib_es5(r)]
    decl_examples = [
        ((r.get("callee") or "")[:60], path_of(r)[-70:])
        for r in no_const
        if is_declaration_only(r)
    ]

    lines: List[str] = []
    lines += [f"# {title} — Callee Resolution Classification", ""]
    lines.append(f"**Source:** eval JSON  ")
    if commit:
        lines.append(f"**Repo commit:** `{commit}`  ")
    lines.append(
        f"**Eval status:** {len(ok)} / {len(all_rows)} ok callee rows "
        f"({summ.get('unique_sample_ids', '?')} samples with callees, "
        f"{summ.get('samples_skipped_no_callees', '?')} skipped)"
    )
    lines += ["", "## Classification rules", "", "| Metric | Rule |", "|--------|------|",
              "| **External libraries** | Definition path contains `node_modules/` |",
              "| **Declaration / interface level** | Outer hit is `.d.ts` or type-only signature, **and** no `runtime_implementation` upgrade |",
              "| **Runtime implementation** | Non-`.d.ts` source with a body, **or** `runtime_implementation.full_def_source` present |",
              "", "---", ""]
    lines += ["## 1. Excluding Prisma, lib.es5.d.ts & const/enum members", "",
              f"**Denominator: {s1['n']}** ok callee rows", "",
              "| Metric | Count | % |", "|--------|------:|--:|",
              f"| External libraries | {s1['ext']} | **{pct(s1['ext'], s1['n']):.1f}%** |",
              f"| Declaration / interface level retrieved | {s1['decl']} | **{pct(s1['decl'], s1['n']):.1f}%** |",
              f"| Runtime implementation retrieved | {s1['runtime']} | **{pct(s1['runtime'], s1['n']):.1f}%** |", ""]
    lines += ["### Cross-tab (origin × resolution quality)", "",
              "| Origin | Declaration only | Runtime impl | Total |",
              "|--------|-----------------:|-------------:|------:|",
              f"| **External** (node_modules) | {s1['ext_decl']} ({pct(s1['ext_decl'], s1['ext_n']):.1f}%) | {s1['ext_rt']} ({pct(s1['ext_rt'], s1['ext_n']):.1f}%) | {s1['ext_n']} ({pct(s1['ext_n'], s1['n']):.1f}%) |",
              f"| **Internal** (repo source) | {s1['int_decl']} ({pct(s1['int_decl'], s1['int_n']):.1f}%) | {s1['int_rt']} ({pct(s1['int_rt'], s1['int_n']):.1f}%) | {s1['int_n']} ({pct(s1['int_n'], s1['n']):.1f}%) |", ""]
    lines += [f"### Runtime retrieval breakdown ({s1['runtime']} rows)", "",
              "| Mechanism | Count |", "|-----------|------:|",
              f"| Direct hit on implementation source (`.ts` / `.js` with body) | {s1['mech'].get('direct_impl', 0)} |",
              f"| `.d.ts` upgraded via `runtime_implementation` bundle | {s1['mech'].get('dts_upgraded', 0)} |", ""]
    if decl_examples:
        lines += ["### Remaining declaration-only rows — examples", ""]
        for callee, p in decl_examples[:12]:
            lines.append(f"- `{callee}` → `{p}`")
        lines.append("")
    lines += ["---", "", "## 2. All callees (excl. const/enum members only)", "",
              f"**Denominator: {s2['n']}** ok callee rows", "",
              "| Metric | Count | % |", "|--------|------:|--:|",
              f"| External libraries | {s2['ext']} | **{pct(s2['ext'], s2['n']):.1f}%** |",
              f"| Declaration / interface level retrieved | {s2['decl']} | **{pct(s2['decl'], s2['n']):.1f}%** |",
              f"| Runtime implementation retrieved | {s2['runtime']} | **{pct(s2['runtime'], s2['n']):.1f}%** |", ""]
    lines += ["### Cross-tab (origin × resolution quality)", "",
              "| Origin | Declaration only | Runtime impl | Total |",
              "|--------|-----------------:|-------------:|------:|",
              f"| **External** (node_modules) | {s2['ext_decl']} ({pct(s2['ext_decl'], s2['ext_n']):.1f}%) | {s2['ext_rt']} ({pct(s2['ext_rt'], s2['ext_n']):.1f}%) | {s2['ext_n']} ({pct(s2['ext_n'], s2['n']):.1f}%) |",
              f"| **Internal** (repo source) | {s2['int_decl']} ({pct(s2['int_decl'], s2['int_n']):.1f}%) | {s2['int_rt']} ({pct(s2['int_rt'], s2['int_n']):.1f}%) | {s2['int_n']} ({pct(s2['int_n'], s2['n']):.1f}%) |", ""]
    if prisma_rows or lib_rows:
        lines += ["### Impact of Prisma + lib.es5 on declaration rate", "",
                  "| Group | Rows | Declaration-only |", "|-------|-----:|-----------------:|"]
        if prisma_rows:
            pd = sum(1 for r in prisma_rows if is_declaration_only(r))
            lines.append(f"| Prisma (`.prisma/client`) | {len(prisma_rows)} | {pd} ({pct(pd, len(prisma_rows)):.0f}%) |")
        if lib_rows:
            ld = sum(1 for r in lib_rows if is_declaration_only(r))
            lines.append(f"| `lib.es5.d.ts` builtins | {len(lib_rows)} | {ld} ({pct(ld, len(lib_rows)):.0f}%) |")
        lines.append(f"| Everything else | {s1['n']} | {s1['decl']} ({pct(s1['decl'], s1['n']):.1f}%) |")
        lines.append("")
    for title_sec, iface, denom in [
        ("## 3. % with interface — excluding Prisma, lib.es5 & const/enum", i1, s1["n"]),
        ("## 4. % with interface — all callees (excl. const/enum only)", i2, s2["n"]),
    ]:
        lines += ["---", "", title_sec, "", f"**{denom} callees**", "",
                  "| Scope | Has interface | % |", "|-------|-------------:|--:|"]
        for scope, key in [("Internal", "internal"), ("External", "external"), ("All", "all")]:
            hi, sn = iface[key]
            lines.append(f"| **{scope}** ({sn if scope != 'All' else denom}) | {hi} | **{pct(hi, sn):.1f}%** |")
        lines.append("")
    lines += ["---", "", "## 5. Failed rows (navigation errors)", "",
              f"**{len(failed)}** failed callee rows across **{len({r['sample_id'] for r in failed})}** samples:", ""]
    for err, cnt in Counter((r.get("error") or "unknown")[:70] for r in failed).most_common():
        lines.append(f"- `{err}` — {cnt}")
    lines.append("")
    for r in failed:
        callee = (r.get("callee") or "")[:55]
        lines.append(f"- sample {r.get('sample_id')} · `{callee}` — {r.get('error', '')}")
    if commit:
        lines += ["", f"*Generated at commit `{commit}`.*"]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--commit", type=str, default="")
    ap.add_argument("--title", type=str, default="Eval")
    args = ap.parse_args()
    data = json.loads(args.json.read_text(encoding="utf-8"))
    report = generate_report(data, commit=args.commit, title=args.title)
    args.out.write_text(report, encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
