"""Prepare a TypeScript resolution run (phase 1 of resolve_from_snippet).

This module turns raw resolve inputs into a ready ResolutionContext:

  - parse / clean the callee snippet into a SnippetSelector
  - validate repo + script paths and load source text
  - resolve language id, typescript-language-server command, and workspace URIs
    (repo root + nearest tsconfig/jsconfig folder)

It does not locate the callee in the file, open documents, or talk to the LSP.
Later phases own that work and only need the returned context + empty result shell.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from lsp_client import file_uri
from models import (
    ResolutionContext,
    ResolutionInputs,
    SnippetSelector,
    build_empty_result,
    build_failure_result,
)


@dataclass(frozen=True)
class PrepareOutcome:
    """Phase-1 result.

    On failure, ``context`` is None and ``result["error"]`` is set.
    On success, both ``context`` and ``result`` are populated for later phases.
    """

    result: Dict[str, Any]
    context: Optional[ResolutionContext] = None

    @property
    def ok(self) -> bool:
        return self.context is not None


def snippet_to_selector(snippet: str) -> SnippetSelector:
    """Parse a callee snippet into kind / receiver / name / anchor."""
    s = snippet.strip()
    anchor = s or snippet

    # Treat anything with "(" as a call-like snippet.
    if "(" in s:
        left = s.split("(", 1)[0].strip()
        if "." in left:
            recv, nm = left.rsplit(".", 1)
            return SnippetSelector(
                kind="call",
                receiver=recv.strip() or None,
                name=nm.strip(),
                anchor=anchor,
            )
        return SnippetSelector(
            kind="call",
            receiver=None,
            name=left or s,
            anchor=anchor,
        )

    # No parentheses: treat "obj.prop" as attribute access.
    if "." in s:
        recv, nm = s.rsplit(".", 1)
        return SnippetSelector(
            kind="attr",
            receiver=recv.strip() or None,
            name=nm.strip(),
            anchor=anchor,
        )

    return SnippetSelector(
        kind="call",
        receiver=None,
        name=s or snippet,
        anchor=anchor,
    )


def nearest_tsconfig_dir(script_path: Path, repo_root: Path) -> Optional[Path]:
    """Walk parents of script_path (within repo_root) for tsconfig/jsconfig."""
    repo = repo_root.resolve()
    cur = script_path.resolve().parent
    names = ("tsconfig.json", "jsconfig.json")
    while True:
        try:
            cur.relative_to(repo)
        except ValueError:
            break
        for cfg_name in names:
            candidate = cur / cfg_name
            if candidate.is_file():
                return cur
        if cur == repo:
            break
        parent = cur.parent
        if parent == cur:
            break
        cur = parent
    return None


def ts_workspace_folder_uris(repo_root: Path, script_path: Path) -> List[str]:
    """Workspace folders for tsserver: repo root, plus nearest package config dir."""
    roots: List[str] = []
    rr = file_uri(repo_root.resolve())
    if rr not in roots:
        roots.append(rr)
    pkg = nearest_tsconfig_dir(script_path, repo_root)
    if pkg is not None:
        u = file_uri(pkg.resolve())
        if u not in roots:
            roots.append(u)
    return roots


def ts_server_cmd() -> List[str]:
    """Resolve typescript-language-server (--stdio), preferring local node_modules."""
    local = (Path("node_modules") / ".bin" / "typescript-language-server").resolve()
    if local.exists():
        return [str(local), "--stdio"]

    path = shutil.which("typescript-language-server")
    if path:
        return [path, "--stdio"]

    raise RuntimeError("typescript-language-server not found;")


def language_id_for_path(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in (".ts", ".tsx", ".mts", ".cts"):
        return "typescript"
    return "javascript"


def prepare_resolution(
    *,
    repo_root: Path,
    script_path: Path,
    tested_function: str,
    snippet: str,
    anchor: Optional[str] = None,
    window: int = 3,
    server_cmd: Optional[List[str]] = None,
    use_go_to_source_definition: bool = True,
) -> PrepareOutcome:
    """Run phase 1: validate inputs, parse callee, build ResolutionContext."""
    repo_root = repo_root.resolve()
    script_path = script_path.resolve()

    selector = snippet_to_selector(snippet)
    inputs = ResolutionInputs(
        repo_root=repo_root,
        file_path=script_path,
        tested_function=tested_function,
        callee=snippet,
        search_text=anchor or selector.anchor,
        window=window,
        selector=selector,
        go_to_source_definition=use_go_to_source_definition,
    )
    result = build_empty_result(inputs)

    if not repo_root.exists():
        return PrepareOutcome(
            result=build_failure_result(result, error=f"repo root not found: {repo_root}")
        )
    if not script_path.exists():
        return PrepareOutcome(
            result=build_failure_result(result, error=f"script path not found: {script_path}")
        )

    try:
        text = script_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return PrepareOutcome(
            result=build_failure_result(result, error=f"Failed to read script: {e}")
        )

    try:
        cmd = list(server_cmd) if server_cmd else ts_server_cmd()
    except RuntimeError as e:
        return PrepareOutcome(result=build_failure_result(result, error=str(e)))

    context = ResolutionContext(
        inputs=inputs,
        text=text,
        doc_uri=file_uri(script_path),
        lang_id=language_id_for_path(script_path),
        cmd=cmd,
        root_uri=file_uri(repo_root),
        workspace_uris=ts_workspace_folder_uris(repo_root, script_path),
    )
    return PrepareOutcome(result=result, context=context)
