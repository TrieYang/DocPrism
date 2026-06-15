"""
C++ (and C) code navigation: resolve a snippet to its definition.
Uses the generic LSP client + clangd.
Install: clangd (e.g. apt install clangd, brew install llvm, or LLVM release)
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from lsp_client import GenericLSPClient, Location, file_uri, uri_to_path


def _clangd_cmd() -> List[str]:
    path = shutil.which("clangd")
    if path:
        return [path]
    return ["clangd"]


def _language_id_for_path(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in (".c", ".h"):
        return "c"
    return "cpp"


def _identifier_from_snippet(snippet: str) -> Optional[str]:
    """Extract the main identifier from snippets like 'foo()', 'obj.method()', 'ns::name()'."""
    s = snippet.strip()
    # Remove trailing ( and args
    if "(" in s:
        s = s.split("(")[0].strip()
    # ns::name or obj.method -> take last segment
    if "::" in s:
        s = s.split("::")[-1].strip()
    if "." in s:
        s = s.split(".")[-1].strip()
    return s if s and all(c.isalnum() or c == "_" for c in s) else None


def _is_cpp_comment_line(line: str) -> bool:
    """True if the line (stripped) looks like a C/C++ comment."""
    s = line.strip()
    return (
        s.startswith("//")
        or s.startswith("/*")
        or s.startswith("*")
        or s.startswith("* ")
        or s.startswith("*/")
    )


def _find_identifier_position(source: str, identifier: str) -> Optional[Tuple[int, int]]:
    """
    Heuristic: find identifier in source. Prefer call site (identifier followed by "(").
    Skip comment lines. Returns (line0, col0) 0-based.
    """
    if not identifier:
        return None
    lines = source.splitlines()
    call_pattern = re.compile(r"\b" + re.escape(identifier) + r"\s*\(")
    word_pattern = re.compile(r"\b" + re.escape(identifier) + r"\b")
    for line0, line in enumerate(lines):
        if _is_cpp_comment_line(line):
            continue
        m = call_pattern.search(line)
        if m:
            return (line0, m.start())
    for line0, line in enumerate(lines):
        if _is_cpp_comment_line(line):
            continue
        m = word_pattern.search(line)
        if m:
            return (line0, m.start())
    return None


def _read_definition_source(loc: Location, num_lines_context: int = 80) -> Optional[str]:
    """Read the file at the definition location and return a region around it."""
    try:
        p = uri_to_path(loc.uri)
        if not p.exists():
            return None
        text = p.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        start = max(0, loc.start_line - 2)
        end = min(len(lines), loc.end_line + 1 + num_lines_context)
        return "\n".join(lines[start:end])
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
) -> Dict[str, Any]:
    """
    Resolve a code snippet (e.g. "get_value()" or "Foo::bar()") to its definition.
    Returns the same JSON shape as code_navigation_Python for DocPrism.
    """
    repo_root = repo_root.resolve()
    script_path = script_path.resolve()

    result: Dict[str, Any] = {
        "ok": False,
        "input": {
            "repo_root": str(repo_root),
            "script_path": str(script_path),
            "tested_function": tested_function,
            "snippet": snippet,
            "anchor": anchor or snippet,
        },
        "error": None,
        "matches": {"candidates": [], "anchored": [], "chosen": None},
        "definitions_all": [],
        "definitions_all_filtered": [],
        "chosen_definition_reason": None,
        "definitions": [],
    }

    if not repo_root.exists():
        result["error"] = f"repo root not found: {repo_root}"
        return result
    if not script_path.exists():
        result["error"] = f"script path not found: {script_path}"
        return result

    try:
        text = script_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        result["error"] = f"Failed to read script: {e}"
        return result

    identifier = _identifier_from_snippet(snippet)
    if not identifier:
        result["error"] = f"Could not extract identifier from snippet: {snippet!r}"
        return result

    pos = _find_identifier_position(text, identifier)
    if pos is None:
        result["error"] = f"Identifier {identifier!r} not found in source"
        return result

    line0, col0 = pos
    lines = text.splitlines()
    line_text = lines[line0] if 0 <= line0 < len(lines) else ""

    result["matches"]["candidates"] = [
        {
            "kind": "call",
            "pretty": identifier,
            "expr_src": snippet,
            "ref": {
                "path": str(script_path),
                "line1": line0 + 1,
                "col1": col0 + 1,
                "line0": line0,
                "col0": col0,
            },
            "line_text": line_text,
            "meta": {"pattern": "heuristic_search"},
        }
    ]
    result["matches"]["anchored"] = result["matches"]["candidates"]
    result["matches"]["chosen"] = result["matches"]["candidates"][0]

    cmd = server_cmd or _clangd_cmd()
    root_uri = file_uri(repo_root)
    lang_id = _language_id_for_path(script_path)
    doc_uri = file_uri(script_path)

    # Help clangd find compile_commands.json (e.g. in repo root or build/)
    init_options: Dict[str, Any] = {}
    for comp_db_dir in [repo_root, repo_root / "build"]:
        if (comp_db_dir / "compile_commands.json").exists():
            init_options["compilationDatabasePath"] = str(comp_db_dir)
            break

    try:
        client = GenericLSPClient(
            server_cmd=cmd,
            root_uri=root_uri,
            language_id=lang_id,
            init_options=init_options,
        )
    except Exception as e:
        result["error"] = f"Failed to start LSP server {cmd!r}: {e}"
        return result

    try:
        client.open_document(doc_uri, text)
        locs = client.goto_definition(doc_uri, line0, col0)
    except Exception as e:
        result["error"] = f"LSP definition request failed: {e}"
        return result
    finally:
        client.close()

    result["definitions_all"] = [loc.to_json() for loc in locs]
    result["definitions_all_filtered"] = result["definitions_all"]

    if not locs:
        result["definitions"] = [
            {
                "outer_ok": False,
                "outer_error": "No definition found from clangd",
                "outer_definition": None,
                "argument_usages_resolved": [],
            }
        ]
        return result

    # Prefer repo-local, avoid system/compiler headers
    chosen = locs[0]
    for loc in locs:
        p = uri_to_path(loc.uri)
        pstr = str(p)
        if "/usr/" in pstr or "/opt/" in pstr or "Compiler/" in pstr:
            continue
        try:
            p.resolve().relative_to(repo_root)
            chosen = loc
            break
        except ValueError:
            pass

    result["chosen_definition_reason"] = {
        "note": "first_definition_or_repo_local",
        "total": len(locs),
    }

    full_def_source = _read_definition_source(chosen)
    outer = {
        **chosen.to_json(),
        "directory": str(uri_to_path(chosen.uri).parent),
        "full_def_source": full_def_source,
    }
    try:
        rel = uri_to_path(chosen.uri).resolve().relative_to(repo_root)
        outer["repo_relative_path"] = str(rel.as_posix())
        outer["repo_relative_dir"] = str(rel.parent.as_posix())
    except ValueError:
        pass

    result["definitions"] = [
        {
            "outer_ok": True,
            "outer_error": None,
            "outer_definition": outer,
            "argument_usages_resolved": [],
        }
    ]
    result["ok"] = True
    return result


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--script-path", required=True)
    ap.add_argument("--tested-function", required=True)
    ap.add_argument("--callee", required=True)
    args = ap.parse_args()

    res = resolve_from_snippet(
        repo_root=Path(args.repo_root),
        script_path=Path(args.script_path),
        tested_function=args.tested_function,
        snippet=args.callee,
        anchor=args.callee,
    )
    print(json.dumps(res, indent=2, ensure_ascii=False))
