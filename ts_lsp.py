"""Shared TypeScript language-server client cache.

Used by go-to-source-definition (phase 3) and later LSP definition strategies.
No knowledge of resolution inputs, callees, or result dicts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from lsp_client import GenericLSPClient
from ts_prepare_resolution import ts_workspace_folder_uris

_TS_LSP_CLIENTS: Dict[Tuple[Any, ...], GenericLSPClient] = {}


def ts_lsp_client_cache_key(repo_root: Path, script_path: Path, lang_id: str) -> Tuple[Any, ...]:
    folders = ts_workspace_folder_uris(repo_root, script_path)
    return (lang_id,) + tuple(folders)


def get_or_create_ts_lsp_client(
    repo_root: Path,
    script_path: Path,
    lang_id: str,
    cmd: List[str],
    root_uri: str,
    workspace_uris: List[str],
) -> GenericLSPClient:
    cache_key = ts_lsp_client_cache_key(repo_root, script_path, lang_id)
    cached = _TS_LSP_CLIENTS.get(cache_key)
    if cached is None:
        primary = workspace_uris[0] if workspace_uris else root_uri
        cached = GenericLSPClient(
            server_cmd=cmd,
            root_uri=primary,
            language_id=lang_id,
            init_options={},
            workspace_folder_uris=workspace_uris or None,
        )
        _TS_LSP_CLIENTS[cache_key] = cached
    return cached
