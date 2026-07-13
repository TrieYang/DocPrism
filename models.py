from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

from lsp_client import GenericLSPClient, Location

UsageKind = Literal["call", "attr"]
TestedRange = Tuple[int, int, int, int]  # start_line, start_col, end_line, end_col (0-based)


@dataclass(frozen=True)
class Position:
    line0: int
    col0: int

    def as_ref(self, path: str) -> Dict[str, Any]:
        return {
            "path": path,
            "line0": self.line0,
            "col0": self.col0,
        }


@dataclass(frozen=True)
class SnippetSelector:
    kind: UsageKind
    receiver: Optional[str]
    name: str
    anchor: str

    @property
    def pretty(self) -> str:
        if self.receiver:
            return f"{self.receiver}.{self.name}"
        return self.name


@dataclass
class CalleeLocation:
    match: Position
    calle_start: Position
    expr_src: str
    expr_rng: Optional[TestedRange] = None


@dataclass(frozen=True)
class DefCandidate:
    loc: Location
    path: Path
    is_d_ts: bool
    in_node_modules: bool


@dataclass
class StrategyResult:
    strategy: str
    chosen_def: DefCandidate
    full_def_source: str
    chosen_definition_reason: Dict[str, Any]
    client: Optional[GenericLSPClient] = None
    declaration_surface: Optional[Dict[str, Any]] = None
    runtime_implementation: Optional[Dict[str, Any]] = None
    definitions_all: List[Dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class ResolutionInputs:
    """Shared phase-1 facts: echoed in the result and carried by ResolutionContext."""

    repo_root: Path
    file_path: Path
    tested_function: str
    callee: str
    search_text: str
    window: int
    selector: SnippetSelector
    go_to_source_definition: bool = True


@dataclass
class ResolutionContext:
    inputs: ResolutionInputs
    text: str
    doc_uri: str
    lang_id: str
    cmd: List[str]
    root_uri: str
    workspace_uris: List[str]

    expr_rng: Optional[TestedRange] = None
    callee_location: Optional[CalleeLocation] = None
    client: Optional[GenericLSPClient] = None

    @property
    def repo_root(self) -> Path:
        return self.inputs.repo_root

    @property
    def file_path(self) -> Path:
        return self.inputs.file_path

    @property
    def tested_function(self) -> str:
        return self.inputs.tested_function

    @property
    def callee(self) -> str:
        return self.inputs.callee

    @property
    def search_text(self) -> str:
        return self.inputs.search_text

    @property
    def window(self) -> int:
        return self.inputs.window

    @property
    def selector(self) -> SnippetSelector:
        return self.inputs.selector

    @property
    def go_to_source_definition(self) -> bool:
        return self.inputs.go_to_source_definition

    @property
    def symbol_name(self) -> Optional[str]:
        return self.selector.name or None

    @property
    def navigation(self) -> Position:
        if self.callee_location is None:
            raise ValueError("callee not set — run locate_callee first")
        return self.callee_location.calle_start

    @property
    def match(self) -> Position:
        if self.callee_location is None:
            raise ValueError("callee not set — run locate_callee first")
        return self.callee_location.match

    @property
    def prefer_same_document_uri(self) -> Optional[str]:
        if self.selector.kind == "attr" and self.selector.receiver == "this":
            return self.doc_uri
        return None


def build_input(inputs: ResolutionInputs) -> Dict[str, Any]:
    """Minimal input echo — one copy of each concept."""
    input_rec: Dict[str, Any] = {
        "repo_root": str(inputs.repo_root),
        "file_path": str(inputs.file_path),
        "tested_function": inputs.tested_function,
        "callee": inputs.callee,
        "parsed": {
            "kind": inputs.selector.kind,
            "receiver": inputs.selector.receiver,
            "name": inputs.selector.name,
        },
        "options": {
            "window": inputs.window,
            "go_to_source_definition": inputs.go_to_source_definition,
        },
    }
    if inputs.search_text.strip() != inputs.callee.strip():
        input_rec["search_text"] = inputs.search_text
    return input_rec


def build_match_entry(
    *,
    selector: SnippetSelector,
    pos: Position,
    path: str,
    expr_src: str,
    pattern: str,
) -> Dict[str, Any]:
    return {
        "kind": selector.kind,
        "name": selector.pretty,
        "expr_src": expr_src,
        "ref": pos.as_ref(path),
        "pattern": pattern,
    }


def apply_callee_to_result(
    result: Dict[str, Any],
    *,
    candidates: List[Dict[str, Any]],
    chosen: Dict[str, Any],
    navigation: Position,
) -> None:
    result["matches"]["candidates"] = candidates
    result["matches"]["chosen"] = chosen
    result["navigation_position"] = {
        "line0": navigation.line0,
        "col0": navigation.col0,
    }


def build_empty_result(inputs: ResolutionInputs) -> Dict[str, Any]:
    return {
        "ok": False,
        "input": build_input(inputs),
        "error": None,
        "matches": {"candidates": [], "anchored": [], "chosen": None},
        "definitions_all": [],
        "definitions_all_filtered": [],
        "chosen_definition_reason": None,
        "navigation_position": None,
        "definitions": [],
    }


def build_success_result(
    result: Dict[str, Any],
    *,
    chosen_definition_reason: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    result["ok"] = True
    if chosen_definition_reason is not None:
        result["chosen_definition_reason"] = chosen_definition_reason
    return result


def build_failure_result(
    result: Dict[str, Any],
    *,
    error: str,
) -> Dict[str, Any]:
    result["error"] = error
    result["ok"] = False
    return result
