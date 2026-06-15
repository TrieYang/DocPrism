#!/usr/bin/env python3
"""
Build a stratified sample of hoppscotch_eval_results for manual review.

Expects hoppscotch_eval_results.json from run_n8n_code_navigation_eval.py (flat format):
one object per callee row, each the full code_navigation_TypeScript output plus
sample_id, callee_index, tested_function, script_path, callee.

Taxonomy:
  - kind: call (callee contains '(') | attribute
  - outcome: success | fail
  - error_type (when fail): LSP_no_definition | Anchor_not_unique | No_candidates_anchor | ...

From each (kind, error_type) category we take up to SAMPLE_SIZE items (default 20)
and write them to a JSON file for manual inspection.
"""
from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_PATH = SCRIPT_DIR / "hoppscotch_eval_results.json"
OUTPUT_PATH = SCRIPT_DIR / "hoppscotch_eval_samples_by_category.json"
SAMPLE_SIZE = 20
RANDOM_SEED = 42  # Set to None for different sample each run


def is_call(callee_str: str) -> bool:
    """Heuristic: has '(' => function/method call."""
    return "(" in callee_str


def normalize_error(err: str | None) -> str:
    if not err:
        return "success"
    if "No definition found from TypeScript LSP" in err:
        return "LSP_no_definition"
    if "Anchor did not uniquely identify" in err:
        return "Anchor_not_unique"
    if "No candidates found by anchor" in err:
        return "No_candidates_anchor"
    if err.startswith("file not found:"):
        return "file_not_found"
    if "no callee/snippet" in err:
        return "no_callee_snippet"
    return "other"


def outer_definition(row: dict) -> dict:
    defs = row.get("definitions") or []
    if not defs:
        return {}
    return defs[0].get("outer_definition") or {}


def main() -> None:
    with open(RESULTS_PATH, encoding="utf-8") as f:
        data = json.load(f)

    rows: list[dict] = []
    for r in data["results"]:
        od = outer_definition(r)
        callee_str = r.get("callee") or ""
        kind = "call" if is_call(callee_str) else "attribute"
        err_type = normalize_error(r.get("error"))
        rows.append(
            {
                "sample_id": r.get("sample_id"),
                "callee_index": r.get("callee_index"),
                "script_path": r.get("script_path"),
                "tested_function": r.get("tested_function"),
                "callee": r.get("callee"),
                "kind": kind,
                "ok": r.get("ok"),
                "error": r.get("error"),
                "error_type": err_type,
                "repo_relative_path": od.get("repo_relative_path"),
                "definition_path": od.get("path"),
                "full_def_source": od.get("full_def_source"),
            }
        )

    # Group by (kind, error_type)
    by_category: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        key = (row["kind"], row["error_type"])
        by_category[key].append(row)

    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)
    samples: dict[str, list[dict]] = {}
    summary: list[dict] = []

    for (kind, err_type), group in sorted(by_category.items(), key=lambda x: (-len(x[1]), x[0])):
        category_name = f"{kind} | {err_type}"
        n_total = len(group)
        n_take = min(SAMPLE_SIZE, n_total)
        chosen = random.sample(group, n_take)
        samples[category_name] = chosen
        summary.append(
            {
                "category": category_name,
                "total": n_total,
                "sampled": len(chosen),
            }
        )

    out = {
        "summary": summary,
        "sample_size_per_category": SAMPLE_SIZE,
        "random_seed": RANDOM_SEED,
        "eval_format": "flat (run_n8n_code_navigation_eval, hoppscotch.json)",
        "samples_by_category": samples,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {OUTPUT_PATH}")
    print("\nCategory counts (total → sampled):")
    for s in summary:
        print(f"  {s['category']:45} {s['total']:4} → {s['sampled']}")


if __name__ == "__main__":
    main()
