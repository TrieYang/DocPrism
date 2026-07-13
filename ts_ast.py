"""Shared TypeScript/JavaScript tree-sitter bootstrap and node helpers.

Used by callee location (phase 2) and by definition-site AST checks.
Does not know about resolution inputs, LSP, or result dicts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

try:
    from tree_sitter import Language, Parser
    import tree_sitter_typescript as _tsts
    import tree_sitter_javascript as _tsjs

    _TS_LANGUAGE_FACTORIES = {
        "typescript": lambda: Language(_tsts.language_typescript()),
        "tsx": lambda: Language(_tsts.language_tsx()),
        "javascript": lambda: Language(_tsjs.language()),
    }
    _TS_PARSER_CACHE: Dict[str, Any] = {}

    def get_parser(name: str):
        parser = _TS_PARSER_CACHE.get(name)
        if parser is None:
            parser = Parser(_TS_LANGUAGE_FACTORIES[name]())
            _TS_PARSER_CACHE[name] = parser
        return parser

    TREE_SITTER_AVAILABLE = True
except ImportError:
    try:
        from tree_sitter_languages import get_parser  # type: ignore

        TREE_SITTER_AVAILABLE = True
    except ImportError:
        TREE_SITTER_AVAILABLE = False

        def get_parser(name: str):  # type: ignore[misc]
            raise RuntimeError("tree-sitter is not available")


def get_ts_parser(script_path: Path):
    """Return a tree-sitter parser for the path's language, or None."""
    if not TREE_SITTER_AVAILABLE:
        return None
    ext = script_path.suffix.lower()
    if ext == ".tsx":
        return get_parser("tsx")
    if ext in (".ts", ".mts", ".cts"):
        return get_parser("typescript")
    if ext in (".js", ".jsx", ".mjs", ".cjs"):
        return get_parser("javascript")
    return None


def node_text(source_bytes: bytes, node) -> str:
    if node is None or node.start_byte is None or node.end_byte is None:
        return ""
    return source_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace")


def point_contained_in_node(row: int, col: int, node) -> bool:
    """True if (row, col) is inside node's range. Tree-sitter end_point is exclusive."""
    if node is None:
        return False
    sr, sc = node.start_point
    er, ec = node.end_point
    if (row, col) < (sr, sc):
        return False
    if (row, col) >= (er, ec):
        return False
    return True


def find_node_at_point(node, row: int, col: int):
    """Smallest tree-sitter node containing (row, col), or None."""
    if node is None or not point_contained_in_node(row, col, node):
        return None
    for i in range(node.child_count):
        child = node.child(i)
        if point_contained_in_node(row, col, child):
            return find_node_at_point(child, row, col)
    return node


def ancestors_include_type(root, target_node, node_types: Tuple[str, ...]) -> bool:
    if root is None or target_node is None:
        return False
    if root.start_byte == target_node.start_byte and root.end_byte == target_node.end_byte:
        return root.type in node_types
    for i in range(root.child_count):
        child = root.child(i)
        if child.start_byte <= target_node.start_byte and child.end_byte >= target_node.end_byte:
            if child.type in node_types:
                return True
            return ancestors_include_type(child, target_node, node_types)
    return False


def point_in_range(
    row: int,
    col: int,
    tested_rng: Optional[Tuple[int, int, int, int]],
) -> bool:
    if tested_rng is None:
        return True
    start_line, start_col, end_line, end_col = tested_rng
    if row < start_line or row > end_line:
        return False
    if row == start_line and col < start_col:
        return False
    if row == end_line and col > end_col:
        return False
    return True
