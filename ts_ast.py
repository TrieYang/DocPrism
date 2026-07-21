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


# Innermost declaration/definition forms we expand an LSP name-span into.
# Prefer these over class/module containers so a method doesn't become the whole class.
# Ambient / signature-only forms (.d.ts stubs) are intentionally excluded — those are
# kept as stubs and handed to heuristics for a real implementation.
_DEFINITION_NODE_TYPES = frozenset(
    {
        "function_declaration",
        "generator_function_declaration",
        "generator_function",
        "method_definition",
        "function",
        "arrow_function",
        "class_declaration",
        "abstract_class_declaration",
        "class",
        "interface_declaration",
        "type_alias_declaration",
        "enum_declaration",
        "public_field_definition",
        "property_signature",
        "method_signature",
        "abstract_method_signature",
        "optional_parameter",
        "required_parameter",
        "rest_parameter",
        "lexical_declaration",
        "variable_declaration",
    }
)

# Prefer the outer wrapper when it carries the full declaration text.
_WRAPPER_PARENT_TYPES = {
    "lexical_declaration": "export_statement",
    "variable_declaration": "export_statement",
}

# Nodes that mean "type/signature only" (not a runtime body). Used so heuristics
# know to try finding a real implementation.
_TYPE_OR_SIGNATURE_NODE_TYPES = frozenset(
    {
        "ambient_declaration",
        "function_signature",
        "interface_declaration",
        "type_alias_declaration",
        "method_signature",
        "abstract_method_signature",
        "property_signature",
    }
)


def enclosing_definition_node(root, row: int, col: int):
    """Smallest tree-sitter declaration node containing (row, col), or None.

    LSP ``textDocument/definition`` typically returns only the identifier span.
    Climb from that point to the enclosing function/method/const/etc. node so
    callers can read the full body via the node's byte range.
    """
    leaf = find_node_at_point(root, row, col)
    if leaf is None:
        return None

    found = None
    node = leaf
    while node is not None:
        if node.type in _DEFINITION_NODE_TYPES:
            found = node
            break
        node = node.parent

    if found is None:
        return None

    wrapper = _WRAPPER_PARENT_TYPES.get(found.type)
    if wrapper is not None:
        parent = found.parent
        if parent is not None and parent.type == wrapper:
            return parent

    return found


def is_type_or_signature_surface_at(path: Path, line0: int, col0: int) -> bool:
    """True if (line0, col0) sits in a type/signature-only AST node (e.g. declare/interface)."""
    parser = get_ts_parser(path)
    if parser is None:
        return False
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    if not source:
        return False
    source_bytes = source.encode("utf-8")
    try:
        tree = parser.parse(source_bytes)
    except Exception:
        return False
    if tree.root_node is None:
        return False

    leaf = find_node_at_point(tree.root_node, line0, col0)
    node = leaf
    while node is not None:
        if node.type in _TYPE_OR_SIGNATURE_NODE_TYPES:
            return True
        # Real implementation forms — stop; not a type-only surface.
        if node.type in (
            "method_definition",
            "function_declaration",
            "generator_function_declaration",
            "generator_function",
            "function",
            "arrow_function",
            "class_declaration",
            "abstract_class_declaration",
            "class",
            "enum_declaration",
            "lexical_declaration",
            "variable_declaration",
            "public_field_definition",
        ):
            return False
        node = node.parent
    return False


def definition_source_via_ast(
    path: Path,
    line0: int,
    col0: int,
) -> Optional[str]:
    """Return full declaration text at (line0, col0) using tree-sitter, or None."""
    parser = get_ts_parser(path)
    if parser is None:
        return None
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not source:
        return None
    source_bytes = source.encode("utf-8")
    try:
        tree = parser.parse(source_bytes)
    except Exception:
        return None
    if tree.root_node is None:
        return None

    node = enclosing_definition_node(tree.root_node, line0, col0)
    if node is None:
        return None
    text = node_text(source_bytes, node)
    return text if text.strip() else None
