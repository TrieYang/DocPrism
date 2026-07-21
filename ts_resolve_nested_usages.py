"""Phase 6: resolve nested callee usages inside the primary snippet.

For each nested call/attr found in the callee text, run LSP definition and
attach the results under ``argument_usages_resolved``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from models import PrimaryDefinition, ResolutionContext, build_success_result
from ts_definition_ops import (
    _choose_one_definition,
    _get_referenced_type_on_line,
    _nested_usages_in_snippet,
)
from ts_locate_callee import nested_usage_to_file_line_col


@dataclass(frozen=True)
class NestedUsagesOutcome:
    """Phase-6 result (terminal for the standard LSP resolve pipeline)."""

    result: Dict[str, Any]
    context: ResolutionContext

    @property
    def ok(self) -> bool:
        return bool(self.result.get("ok"))


def resolve_nested_usages(
    ctx: ResolutionContext,
    result: Dict[str, Any],
    primary: PrimaryDefinition,
) -> NestedUsagesOutcome:
    """Run phase 6: nested usages, then finish the success result."""
    from code_navigation_TypeScript import _read_definition_source

    client = ctx.client
    nav = ctx.navigation
    match_pos = ctx.match
    expr_src = (
        ctx.callee_location.expr_src
        if ctx.callee_location is not None
        else ctx.search_text
    )
    outer = primary.outer_definition
    outer_item: Dict[str, Any] = primary.outer_item or {
        "outer_ok": False,
        "outer_error": None,
        "outer_definition": None,
        "argument_usages_resolved": [],
    }

    nested_recs: List[Dict[str, Any]] = []
    if client is not None:
        for u in _nested_usages_in_snippet(ctx.callee, ctx.selector.name):
            try:
                n_line0, n_col0 = nested_usage_to_file_line_col(
                    ctx.text,
                    ctx.callee,
                    nav.line0,
                    match_pos.col0,
                    int(u["offset"]),
                    expr_src,
                )
                u_locs = client.goto_definition(ctx.doc_uri, n_line0, n_col0)

                prefer_nested_doc = (
                    ctx.doc_uri
                    if u.get("kind") == "attr" and u.get("receiver") == "this"
                    else None
                )
                chosen_u, debug_u = _choose_one_definition(
                    ctx.repo_root,
                    u_locs,
                    symbol_name=u["name"] if u.get("kind") == "call" else None,
                    usage_kind=u.get("kind"),
                    prefer_same_document_uri=prefer_nested_doc,
                )
                rec: Dict[str, Any] = {
                    "usage": {
                        "kind": u["kind"],
                        "name": u["name"],
                        "receiver": u["receiver"],
                        "line0": n_line0,
                        "col0": n_col0,
                        "node_line0": n_line0,
                        "pattern": u["pattern"],
                    },
                    "definitions_all": [L.to_json() for L in u_locs],
                    "chosen_definition_reason": debug_u,
                    "definition": None,
                    "ok": False,
                    "error": None,
                }

                if not u_locs:
                    rec["error"] = "no_definitions_from_lsp"
                elif chosen_u is None:
                    rec["error"] = "no_valid_implementation_after_filtering"
                else:
                    uloc = chosen_u.loc
                    upath = chosen_u.path
                    ddef: Dict[str, Any] = {**uloc.to_json()}
                    ddef["path"] = upath.as_posix()
                    ddef["directory"] = upath.parent.as_posix()
                    try:
                        urel = upath.resolve().relative_to(ctx.repo_root.resolve())
                        ddef["repo_relative_path"] = urel.as_posix()
                        ddef["repo_relative_dir"] = urel.parent.as_posix()
                    except Exception:
                        pass
                    full_src = _read_definition_source(
                        uloc,
                        u["name"] if u.get("kind") == "call" else None,
                    )
                    # For single-line property/field declarations (e.g. "x: TypeName;"),
                    # resolve the referenced type and use its full source.
                    if (
                        u.get("kind") == "attr"
                        and full_src
                        and "\n" not in full_src
                        and full_src.strip().endswith(";")
                    ):
                        try:
                            def_lines = upath.read_text(encoding="utf-8", errors="replace").splitlines()
                            if 0 <= uloc.start_line < len(def_lines):
                                line = def_lines[uloc.start_line]
                                type_info = _get_referenced_type_on_line(line)
                                if type_info:
                                    type_name, type_col = type_info
                                    type_locs = client.goto_definition(
                                        uloc.uri, uloc.start_line, type_col
                                    )
                                    if not type_locs:
                                        type_locs = client.goto_type_definition(
                                            uloc.uri, uloc.start_line, type_col
                                        )
                                    if type_locs:
                                        type_loc = type_locs[0]
                                        type_src = _read_definition_source(type_loc, type_name)
                                        if type_src:
                                            full_src = type_src
                                        elif (
                                            type_loc.uri != uloc.uri
                                            or type_loc.start_line != uloc.start_line
                                        ):
                                            type_src = _read_definition_source(type_loc, None)
                                            if type_src:
                                                full_src = type_src
                        except Exception:
                            pass
                    ddef["full_def_source"] = full_src
                    try:
                        ddef["callee_documentation"] = client.hover(
                            uloc.uri, uloc.start_line, uloc.start_col
                        )
                    except Exception:
                        ddef["callee_documentation"] = None
                    rec["definition"] = ddef
                    rec["ok"] = True

                nested_recs.append(rec)
            except Exception as e:
                nested_recs.append(
                    {
                        "usage": u,
                        "definitions_all": [],
                        "chosen_definition_reason": {"note": "nested_resolution_failed"},
                        "definition": None,
                        "ok": False,
                        "error": f"{type(e).__name__}: {e}",
                    }
                )

    outer_item["outer_ok"] = True
    outer_item["outer_definition"] = outer
    outer_item["argument_usages_resolved"] = nested_recs
    result["definitions"] = [outer_item]
    build_success_result(result)
    return NestedUsagesOutcome(result=result, context=ctx)
