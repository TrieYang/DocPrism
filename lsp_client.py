"""
Generic LSP client for "go to definition" and related operations.
Shared by all language-specific code navigators (Python, TypeScript, etc.).
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


def _encode_lsp(msg: Dict[str, Any]) -> bytes:
    body = json.dumps(msg, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
    return header + body


def _read_lsp_message(stream) -> Dict[str, Any]:
    headers: Dict[str, str] = {}
    while True:
        line = stream.readline()
        if not line:
            raise EOFError("LSP server closed the stream.")
        line = line.decode("ascii", errors="replace").strip()
        if line == "":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    if "content-length" not in headers:
        raise ValueError(f"Missing Content-Length header. Got headers={headers}")

    length = int(headers["content-length"])
    body = stream.read(length)
    if not body:
        raise EOFError("No body received from LSP server.")
    return json.loads(body.decode("utf-8"))


def file_uri(path: Path) -> str:
    return path.resolve().as_uri()


def uri_to_path(uri: str) -> Path:
    if not uri.startswith("file://"):
        raise ValueError(f"Unsupported URI: {uri}")
    from urllib.parse import unquote, urlparse
    parsed = urlparse(uri)
    return Path(unquote(parsed.path))


@dataclass(frozen=True)
class Location:
    uri: str
    start_line: int
    start_char: int
    end_line: int
    end_char: int

    def to_json(self) -> Dict[str, Any]:
        return {
            "uri": self.uri,
            "path": str(uri_to_path(self.uri)),
            "range": {
                "start": {"line0": self.start_line, "col0": self.start_char},
                "end": {"line0": self.end_line, "col0": self.end_char},
            },
        }


def _parse_location_or_link(x: Dict[str, Any]) -> Location:
    if "targetUri" in x:
        uri = x["targetUri"]
        rng = x.get("targetSelectionRange") or x.get("targetRange")
    else:
        uri = x["uri"]
        rng = x["range"]
    return Location(
        uri=uri,
        start_line=rng["start"]["line"],
        start_char=rng["start"]["character"],
        end_line=rng["end"]["line"],
        end_char=rng["end"]["character"],
    )


def as_locations(result: Any) -> List[Location]:
    if result is None:
        return []
    if isinstance(result, dict):
        return [_parse_location_or_link(result)]
    if isinstance(result, list):
        return [_parse_location_or_link(x) for x in result]
    return []


class GenericLSPClient:
    """
    Language-agnostic LSP client. Talks to any LSP server over stdio.
    Use for textDocument/definition (and optionally other methods).
    """

    def __init__(
        self,
        server_cmd: List[str],
        root_uri: str,
        language_id: str,
        init_options: Optional[Dict[str, Any]] = None,
        workspace_folder_uris: Optional[List[str]] = None,
    ):
        self.root_uri = root_uri
        self.language_id = language_id
        self._init_options = init_options or {}
        self._id = 0
        self._workspace_folder_uris: List[str] = (
            list(workspace_folder_uris) if workspace_folder_uris else [root_uri]
        )
        if not self._workspace_folder_uris:
            self._workspace_folder_uris = [root_uri]

        self.proc = subprocess.Popen(
            server_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            # Do not pipe stderr unless draining it; some language servers can
            # fill this buffer and stall responses.
            stderr=subprocess.DEVNULL,
        )
        assert self.proc.stdin is not None and self.proc.stdout is not None
        self._initialize()

    def close(self) -> None:
        if self.proc.poll() is None:
            try:
                self._notify("exit", {})
            except Exception:
                pass
            try:
                self.proc.kill()
            except Exception:
                pass

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    def _send(self, msg: Dict[str, Any]) -> None:
        assert self.proc.stdin is not None
        self.proc.stdin.write(_encode_lsp(msg))
        self.proc.stdin.flush()

    def _request(self, method: str, params: Dict[str, Any]) -> Any:
        req_id = self._next_id()
        self._send({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params})
        while True:
            msg = _read_lsp_message(self.proc.stdout)
            if "id" in msg and msg.get("id") == req_id:
                if "error" in msg:
                    raise RuntimeError(f"LSP error: {msg['error']}")
                return msg.get("result")

    def _notify(self, method: str, params: Dict[str, Any]) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def _initialize(self) -> None:
        primary = self._workspace_folder_uris[0]
        folders = []
        for i, uri in enumerate(self._workspace_folder_uris):
            if uri.startswith("file://"):
                try:
                    name = uri_to_path(uri).name or f"root{i}"
                except ValueError:
                    name = f"root{i}"
            else:
                name = Path(uri).name or f"root{i}"
            folders.append({"uri": uri, "name": name})
        self._request(
            "initialize",
            {
                "rootUri": primary,
                "capabilities": {},
                "initializationOptions": self._init_options,
                "workspaceFolders": folders,
            },
        )
        self._notify("initialized", {})

    def goto_implementation(self, doc_uri: str, line0: int, col0: int) -> List[Location]:
        result = self._request(
            "textDocument/implementation",
            {
                "textDocument": {"uri": doc_uri},
                "position": {"line": line0, "character": col0},
            },
        )
        return as_locations(result)

    def goto_type_definition(self, doc_uri: str, line0: int, col0: int) -> List[Location]:
        result = self._request(
            "textDocument/typeDefinition",
            {
                "textDocument": {"uri": doc_uri},
                "position": {"line": line0, "character": col0},
            },
        )
        return as_locations(result)

    def hover(self, doc_uri: str, line0: int, col0: int) -> Optional[str]:
        result = self._request(
            "textDocument/hover",
            {
                "textDocument": {"uri": doc_uri},
                "position": {"line": line0, "character": col0},
            },
        )
        if result is None:
            return None
        contents = result.get("contents")
        if contents is None:
            return None
        if isinstance(contents, dict) and "value" in contents:
            return contents.get("value") or None
        if isinstance(contents, str):
            return contents if contents.strip() else None
        if isinstance(contents, list):
            parts = []
            for item in contents:
                if isinstance(item, dict) and "value" in item:
                    parts.append(item.get("value", ""))
                elif isinstance(item, str):
                    parts.append(item)
            return "\n\n".join(parts).strip() or None
        return None

    def open_document(self, file_uri: str, text: str) -> None:
        self._notify(
            "textDocument/didOpen",
            {
                "textDocument": {
                    "uri": file_uri,
                    "languageId": self.language_id,
                    "version": 1,
                    "text": text,
                }
            },
        )

    def goto_definition(self, doc_uri: str, line0: int, col0: int) -> List[Location]:
        """LSP uses 0-based line and character. Pass line0, col0 (0-based)."""
        result = self._request(
            "textDocument/definition",
            {
                "textDocument": {"uri": doc_uri},
                "position": {"line": line0, "character": col0},
            },
        )
        return as_locations(result)

    def execute_command(self, command: str, arguments: List[Any]) -> Any:
        """Run workspace/executeCommand (e.g. typescript-language-server extensions)."""
        return self._request(
            "workspace/executeCommand",
            {"command": command, "arguments": arguments},
        )

    def goto_source_definition(self, doc_uri: str, line0: int, col0: int) -> List[Location]:
        """
        TypeScript 4.7+ Go to Source Definition (via typescript-language-server).

        Skips declaration files (.d.ts) and tries to land in .ts/.js implementation
        sources. Requires TS 4.7+ and typescript-language-server >= 1.1.0.
        """
        try:
            result = self.execute_command(
                "_typescript.goToSourceDefinition",
                [doc_uri, {"line": line0, "character": col0}],
            )
            return as_locations(result)
        except Exception:
            return []

    def document_symbols(self, doc_uri: str) -> Any:
        """
        Fetch document symbols for the given document.

        The return value is the raw LSP response which may be either:
        - a list of DocumentSymbol objects, or
        - a list of SymbolInformation objects.
        """
        return self._request(
            "textDocument/documentSymbol",
            {
                "textDocument": {"uri": doc_uri},
            },
        )
