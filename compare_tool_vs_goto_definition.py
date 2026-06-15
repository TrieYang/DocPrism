#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent


def _norm_source(s: Optional[str]) -> str:
    if not s:
        return ""
    return "\n".join(line.rstrip() for line in s.splitlines()).strip()


def _outer_full_def(row: Dict[str, Any]) -> Optional[str]:
    defs = row.get("definitions") or []
    if not defs:
        return None
    od = defs[0].get("outer_definition") or {}
    return od.get("full_def_source")


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare tool full_def_source vs LSP go-to-definition")
    ap.add_argument(
        "--results",
        type=Path,
        default=SCRIPT_DIR / "hoppscotch_eval_results.json",
        help="Flat eval JSON from run_n8n_code_navigation_eval.py",
    )
    ap.add_argument("--limit", type=int, default=None, help="Max rows to compare (default: all)")
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Write JSON report (summary + mismatch details)",
    )
    ap.add_argument(
        "--sleep",
        type=float,
        default=0.12,
        help="Seconds after didOpen before definition request (tsserver warm-up)",
    )
    args = ap.parse_args()

    sys.path.insert(0, str(SCRIPT_DIR))
    from code_navigation_TypeScript import (  # noqa: E402
        _read_definition_source,
        _ts_server_cmd,
        file_uri,
        resolve_from_snippet,
        ts_workspace_folder_uris,
    )
    from lsp_client import GenericLSPClient  # noqa: E402

    path = args.results
    if not path.is_file():
        print(f"Results file not found: {path}", file=sys.stderr)
        return 1

    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    rows: List[Dict[str, Any]] = data.get("results") or []
    if args.limit is not None:
        rows = rows[: args.limit]

    if not rows:
        print("No rows to compare.")
        return 0

    # One LSP client for the repo (workspace folders from first script path).
    first_script = Path(rows[0].get("script_path") or rows[0].get("input", {}).get("script_path", ""))
    repo_root = Path(rows[0].get("input", {}).get("repo_root", ""))
    if not repo_root.is_dir():
        print("Could not infer repo_root from first row.", file=sys.stderr)
        return 1
    repo_root = repo_root.resolve()
    if not first_script.is_file():
        print("Could not infer script_path from first row.", file=sys.stderr)
        return 1
    first_script = first_script.resolve()

    uris = ts_workspace_folder_uris(repo_root, first_script)
    client = GenericLSPClient(
        server_cmd=_ts_server_cmd(),
        root_uri=uris[0],
        language_id="typescript",
        workspace_folder_uris=uris,
    )

    summary = {
        "results_file": str(path),
        "limit": args.limit,
        "total_rows": len(rows),
        "compared": 0,
        "match": 0,
        "mismatch": 0,
        "no_tool_source": 0,
        "no_navigation_position": 0,
        "no_definition_from_lsp": 0,
        "resolve_errors": 0,
    }
    mismatches: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []

    try:
        for row in rows:
            inp = row.get("input") or {}
            script_path = Path(row.get("script_path") or inp.get("script_path", ""))
            tested = row.get("tested_function") or inp.get("tested_function")
            callee = row.get("callee")
            usage = inp.get("usage") or {}
            symbol_name = usage.get("name") or ""

            if not script_path.is_file() or not tested or callee is None:
                summary["resolve_errors"] += 1
                errors.append({"reason": "missing_path_or_callee", "sample_id": row.get("sample_id")})
                continue

            try:
                res = resolve_from_snippet(
                    repo_root=repo_root,
                    script_path=script_path,
                    tested_function=tested,
                    snippet=callee,
                    anchor=callee,
                )
            except Exception as e:
                summary["resolve_errors"] += 1
                errors.append(
                    {
                        "reason": f"resolve_from_snippet:{e}",
                        "sample_id": row.get("sample_id"),
                        "callee_index": row.get("callee_index"),
                    }
                )
                continue

            pos = res.get("navigation_position")
            if not pos:
                summary["no_navigation_position"] += 1
                continue

            tool_src = _outer_full_def(res)
            if not tool_src:
                summary["no_tool_source"] += 1
                continue

            doc_uri = file_uri(script_path.resolve())
            try:
                text = script_path.read_text(encoding="utf-8", errors="replace")
            except OSError as e:
                summary["resolve_errors"] += 1
                errors.append({"reason": str(e), "sample_id": row.get("sample_id")})
                continue

            client.open_document(doc_uri, text)
            time.sleep(args.sleep)

            try:
                locs = client.goto_definition(doc_uri, int(pos["line0"]), int(pos["col0"]))
            except Exception as e:
                summary["resolve_errors"] += 1
                errors.append(
                    {
                        "reason": f"goto_definition:{e}",
                        "sample_id": row.get("sample_id"),
                        "callee_index": row.get("callee_index"),
                    }
                )
                continue

            if not locs:
                summary["no_definition_from_lsp"] += 1
                ide_src = None
            else:
                ide_src = _read_definition_source(locs[0], symbol_name or None)

            summary["compared"] += 1
            a, b = _norm_source(tool_src), _norm_source(ide_src)
            if a == b:
                summary["match"] += 1
            else:
                summary["mismatch"] += 1
                mismatches.append(
                    {
                        "sample_id": row.get("sample_id"),
                        "callee_index": row.get("callee_index"),
                        "tested_function": tested,
                        "callee_preview": (callee[:120] + "…") if len(callee) > 120 else callee,
                        "position": pos,
                        "definition_uri_first": locs[0].uri if locs else None,
                        "tool_norm_len": len(a),
                        "ide_norm_len": len(b),
                        "tool_preview": a[:400] + ("…" if len(a) > 400 else ""),
                        "ide_preview": b[:400] + ("…" if len(b) > 400 else ""),
                    }
                )
    finally:
        client.close()

    pct = 100.0 * summary["match"] / summary["compared"] if summary["compared"] else 0.0
    print("--- compare_tool_vs_goto_definition ---")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    if summary["compared"]:
        print(f"  match_rate_percent: {pct:.1f}")

    if args.out:
        out_obj = {"summary": summary, "mismatches": mismatches, "errors": errors[:50]}
        args.out.write_text(json.dumps(out_obj, indent=2), encoding="utf-8")
        print(f"\nWrote {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
