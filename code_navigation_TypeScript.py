from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from lsp_client import Location, uri_to_path
from ts_ast import definition_source_via_ast
from ts_locate_callee import locate_callee
from ts_prepare_resolution import (  # noqa: F401 — re-exported public helpers
    prepare_resolution,
    ts_server_cmd as _ts_server_cmd,
)
from ts_resolve_nested_usages import resolve_nested_usages
from ts_resolve_primary import resolve_primary_definition


def _source_from_lsp_range(loc: Location) -> Optional[str]:
    """Keep the stub text covered by the raw LSP range (usually one line)."""
    path = uri_to_path(loc.uri)
    if not path.exists():
        return None
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines:
        return None
    start = max(0, min(loc.start_line, len(lines) - 1))
    end = max(start, min(loc.end_line, len(lines) - 1))
    text = "\n".join(lines[start : end + 1])
    return text if text.strip() else None


def _read_definition_source(
    loc: Location,
    symbol_name: Optional[str] = None,
    *,
    usage_hint: Optional[str] = None,
) -> Optional[str]:
    """ 
    Prefer tree-sitter expansion to the full enclosing body. When that fails
    keep the LSP range as a stub
    
    so later heuristics can try for a real implementation and still fall back
    to this text if they cannot.
    """
    del symbol_name, usage_hint  # unused — kept for callers
    try:
        path = uri_to_path(loc.uri)
        if not path.exists():
            return None
        expanded = definition_source_via_ast(path, loc.start_line, loc.start_col)
        if expanded:
            return expanded
        # Expansion missed (common for ambient .d.ts stubs) — keep the stub.
        return _source_from_lsp_range(loc)
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

    #---phase 3: primary resolve (source def/defi/heuristics)---#
    primary = resolve_primary_definition(ctx, result)
    result = primary.result
    ctx = primary.context
    if primary.done or primary.primary is None:
        return result

    #---phase 4: nested callee usages, in progress---#
    return resolve_nested_usages(ctx, result, primary.primary).result


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
