"""Newline-aware text coordinate helpers (no language / LSP knowledge)."""

from __future__ import annotations

from typing import Tuple


def is_comment_line(line: str) -> bool:
    s = line.strip()
    return s.startswith("//") or s.startswith("*") or s.startswith("/*") or s.startswith("* ")


def char_index_from_line_col(text: str, line0: int, col0: int) -> int:
    """0-based (line, col) -> character index in text (newline-aware)."""
    i = 0
    ln = 0
    n = len(text)
    while ln < line0 and i < n:
        j = text.find("\n", i)
        if j < 0:
            return n
        i = j + 1
        ln += 1
    return i + col0


def line_col_from_char_index(text: str, index: int) -> Tuple[int, int]:
    """Character index in text -> 0-based (line0, col0)."""
    index = max(0, min(index, len(text)))
    prefix = text[:index]
    line0 = prefix.count("\n")
    last_nl = prefix.rfind("\n")
    col0 = index - (last_nl + 1) if last_nl >= 0 else index
    return line0, col0


def raw_index_to_flat_index(text: str, raw_i: int) -> int:
    """Map index in raw text (possible \\r\\n) to index in text.replace('\\r\\n', '\\n')."""
    fi = 0
    ri = 0
    n = len(text)
    target = max(0, min(raw_i, n))
    while ri < target:
        if ri + 1 < n and text[ri] == "\r" and text[ri + 1] == "\n":
            ri += 2
            fi += 1
        else:
            ri += 1
            fi += 1
    return fi


def flat_index_to_raw_index(text: str, flat_i: int) -> int:
    """Inverse of raw_index_to_flat_index."""
    fi = 0
    ri = 0
    n = len(text)
    target = max(0, flat_i)
    while fi < target and ri < n:
        if ri + 1 < n and text[ri] == "\r" and text[ri + 1] == "\n":
            ri += 2
            fi += 1
        else:
            ri += 1
            fi += 1
    return ri
