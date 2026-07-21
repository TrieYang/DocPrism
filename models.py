from __future__ import annotations

from dataclasses import dataclass
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
    """Where the callee was found in the usage file (phase 2)."""

    match: Position
    callee_start: Position
    expr_src: str
    pattern: str
    expr_rng: Optional[TestedRange] = None


@dataclass(frozen=True)
class DefCandidate:
    loc: Location
    path: Path
    is_d_ts: bool
    in_node_modules: bool
    is_repo_local: bool = False
    path_len: int = 0


@dataclass
class PrimaryDefinition:
    """Primary definition ready for nested-usage resolution."""

    chosen_def: DefCandidate
    full_def_source: Optional[str]
    symbol_name: Optional[str]
    receiver_parent_hint: Optional[str] = None
    usage_hint: str = ""
    declaration_surface: Optional[Dict[str, Any]] = None
    runtime_implementation: Optional[Dict[str, Any]] = None
    upgraded_from_declaration: bool = False
    outer_definition: Optional[Dict[str, Any]] = None
    # Shell for the final ``definitions[0]`` entry; finished by nested resolution.
    outer_item: Optional[Dict[str, Any]] = None


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
        return self.callee_location.callee_start

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
    line_text: str = "",
) -> Dict[str, Any]:
    """One usage-site candidate/chosen entry (shared JSON shape for result["matches"])."""
    return {
        "kind": selector.kind,
        "pretty": selector.pretty,
        "expr_src": expr_src,
        "ref": {
            "path": path,
            "line1": pos.line0 + 1,
            "col1": pos.col0 + 1,
            "line0": pos.line0,
            "col0": pos.col0,
        },
        "line_text": line_text,
        "meta": {"pattern": pattern},
    }


def apply_callee_to_result(
    result: Dict[str, Any],
    *,
    candidates: List[Dict[str, Any]],
    chosen: Dict[str, Any],
    navigation: Position,
    anchored: Optional[List[Dict[str, Any]]] = None,
) -> None:
    result["matches"]["candidates"] = candidates
    result["matches"]["chosen"] = chosen
    if anchored is not None:
        result["matches"]["anchored"] = anchored
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
