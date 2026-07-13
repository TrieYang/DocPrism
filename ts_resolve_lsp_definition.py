"""Phase 4: resolve via standard LSP definition methods.

Fallback when goToSourceDefinition (phase 3) did not yield a usable result.
Covers definition / typeDefinition / implementation, second-hop fixes,
external runtime upgrade, symbol re-anchoring, and nested usage resolution.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from lsp_client import Location, file_uri, uri_to_path
from models import ResolutionContext, build_failure_result, build_success_result
from ts_definition_ops import (
    _build_def_candidate,
    _build_outer_definition,
    _choose_one_definition,
    _dedupe_locations,
    _definition_location_is_call_site_ast,
    _definition_source_is_import_or_export,
    _definition_source_looks_like_usage,
    _definition_source_matches_symbol,
    _extract_function_range_from_symbols,
    _find_definition_via_imports,
    _find_symbol_location_from_document_symbols,
    _get_referenced_type_on_line,
    _nested_usages_in_snippet,
    _prefer_lib_global_constructor_snippet,
    _try_external_declaration_runtime_upgrade,
)
from ts_locate_callee import nested_usage_to_file_line_col
from ts_lsp import get_or_create_ts_lsp_client


@dataclass(frozen=True)
class LspDefinitionOutcome:
    """Phase-4 result (terminal for the current resolve pipeline)."""

    result: Dict[str, Any]
    context: ResolutionContext

    @property
    def ok(self) -> bool:
        return bool(self.result.get("ok"))


def resolve_via_lsp_definition(
    ctx: ResolutionContext,
    result: Dict[str, Any],
) -> LspDefinitionOutcome:
    """Run phase 4 and return a finished success or failure result."""
    from code_navigation_TypeScript import _read_definition_source

    client = ctx.client
    nav = ctx.navigation
    match_pos = ctx.match
    expr_src = (
        ctx.callee_location.expr_src
        if ctx.callee_location is not None
        else ctx.search_text
    )
    usage_hint = ctx.search_text
    tested_rng = ctx.expr_rng
    prefer_same_doc_uri = ctx.prefer_same_document_uri

    # Standard LSP definition / typeDefinition / implementation.
    outer_item: Dict[str, Any] = {
        "outer_ok": False,
        "outer_error": None,
        "outer_definition": None,
        "argument_usages_resolved": [],
    }

    try:
        if client is None:
            client = get_or_create_ts_lsp_client(
                ctx.repo_root, ctx.file_path, ctx.lang_id, ctx.cmd, ctx.root_uri, ctx.workspace_uris
            )
            ctx.client = client

            client.open_document(ctx.doc_uri, ctx.text)
            time.sleep(0.2)

            if tested_rng is None:
                try:
                    symbols = client.document_symbols(ctx.doc_uri)
                    sym_rng = _extract_function_range_from_symbols(symbols, ctx.tested_function)
                    if sym_rng is not None:
                        tested_rng = sym_rng
                        ctx.expr_rng = tested_rng
                except Exception:
                    pass

        if ctx.selector.kind == "attr":
            locs = []
            locs.extend(client.goto_definition(ctx.doc_uri, nav.line0, nav.col0))
            locs.extend(client.goto_type_definition(ctx.doc_uri, nav.line0, nav.col0))
            locs.extend(client.goto_implementation(ctx.doc_uri, nav.line0, nav.col0))
            locs = _dedupe_locations(locs)
        else:
            locs = []
            locs.extend(client.goto_implementation(ctx.doc_uri, nav.line0, nav.col0))
            if not locs:
                locs.extend(client.goto_definition(ctx.doc_uri, nav.line0, nav.col0))
            # TypeScript often resolves method calls to implementation via typeDefinition
            if not locs:
                locs = client.goto_type_definition(ctx.doc_uri, nav.line0, nav.col0)
            locs = _dedupe_locations(locs)
    except Exception as e:
        return LspDefinitionOutcome(
            result=build_failure_result(result, error=f"LSP definition request failed: {e}"),
            context=ctx,
        )

    result["definitions_all"] = [loc.to_json() for loc in locs]
    result["definitions_all_filtered"] = [loc.to_json() for loc in locs]

    if not locs:
        outer_item["outer_error"] = "No definition found from TypeScript LSP."
        result["definitions"] = [outer_item]
        return LspDefinitionOutcome(
            result=build_failure_result(result, error=outer_item["outer_error"]),
            context=ctx,
        )

    # Use the accessed symbol name for both calls and attributes so candidate
    # validation can reject nearby-but-wrong type/class locations.
    symbol_name_for_choice = ctx.symbol_name
    receiver_parent_hint: Optional[str] = None
    if ctx.selector.receiver:
        # e.g. this.prisma.personalAccessToken.create -> parent hint personalAccessToken
        receiver_parent_hint = ctx.selector.receiver.split(".")[-1].strip() or None
    chosen_def, debug = _choose_one_definition(
        ctx.repo_root,
        locs,
        symbol_name=symbol_name_for_choice,
        usage_kind=ctx.selector.kind,
        prefer_same_document_uri=prefer_same_doc_uri,
    )
    result["chosen_definition_reason"] = debug

    if chosen_def is None:
        outer_item["outer_error"] = "No valid implementation found after filtering."
        result["definitions"] = [outer_item]
        return LspDefinitionOutcome(
            result=build_failure_result(result, error=outer_item["outer_error"]),
            context=ctx,
        )

    full_def_source = _read_definition_source(
        chosen_def.loc,
        symbol_name_for_choice,
        usage_hint=usage_hint,
    )
    full_def_source = _prefer_lib_global_constructor_snippet(
        full_def_source,
        chosen_def.path,
        symbol_name_for_choice,
        usage_kind=ctx.selector.kind,
    )
    # Second hop when LSP landed on a non-definition site (import/re-export or call usage).
    fix_import = bool(
        symbol_name_for_choice
        and _definition_source_is_import_or_export(chosen_def.loc, symbol_name_for_choice)
    )
    fix_call = bool(
        symbol_name_for_choice
        and full_def_source
        and (
            _definition_location_is_call_site_ast(chosen_def.path, chosen_def.loc)
            or _definition_source_looks_like_usage(
                chosen_def.loc,
                symbol_name_for_choice,
                ctx.doc_uri,
                full_def_source,
            )
        )
    )

    if fix_import or fix_call:
        if fix_call:
            found = _find_definition_via_imports(ctx.file_path, symbol_name_for_choice, ctx.repo_root)
            if found:
                def_path_found, def_line0 = found
                loc_found = Location(
                    uri=file_uri(def_path_found),
                    start_line=def_line0,
                    start_col=0,
                    end_line=def_line0,
                    end_col=0,
                )
                chosen_def = _build_def_candidate(ctx.repo_root, loc_found)
                full_def_source = _read_definition_source(
                    loc_found, symbol_name_for_choice, usage_hint=usage_hint
                )
                if full_def_source:
                    result["chosen_definition_reason"] = {
                        **result.get("chosen_definition_reason", {}),
                        "note": "definition_via_imports_followed",
                    }
                    fix_call = bool(
                        _definition_location_is_call_site_ast(chosen_def.path, chosen_def.loc)
                        or _definition_source_looks_like_usage(
                            chosen_def.loc,
                            symbol_name_for_choice,
                            ctx.doc_uri,
                            full_def_source,
                        )
                    )

        fix_import = bool(
            symbol_name_for_choice
            and _definition_source_is_import_or_export(chosen_def.loc, symbol_name_for_choice)
        )
        if fix_import or fix_call:
            try:
                second_locs = client.goto_definition(
                    chosen_def.loc.uri,
                    chosen_def.loc.start_line,
                    chosen_def.loc.start_col,
                )
                if second_locs:
                    if fix_call:
                        second_candidates_with_def = [
                            loc
                            for loc in second_locs
                            if not _definition_location_is_call_site_ast(
                                uri_to_path(loc.uri), loc
                            )
                            and not _definition_source_looks_like_usage(
                                loc,
                                symbol_name_for_choice,
                                ctx.doc_uri,
                                _read_definition_source(
                                    loc,
                                    symbol_name_for_choice,
                                    usage_hint=usage_hint,
                                ),
                            )
                        ]
                        pool = (
                            second_candidates_with_def
                            if second_candidates_with_def
                            else second_locs
                        )
                    else:
                        pool = second_locs
                    second_chosen, _ = _choose_one_definition(
                        ctx.repo_root,
                        pool,
                        symbol_name=symbol_name_for_choice,
                        usage_kind=ctx.selector.kind,
                        prefer_same_document_uri=prefer_same_doc_uri,
                    )
                    if second_chosen is not None:
                        second_src = _read_definition_source(
                            second_chosen.loc,
                            symbol_name_for_choice,
                            usage_hint=usage_hint,
                        )
                        accept = bool(second_src)
                        if accept and fix_import:
                            accept = not _definition_source_is_import_or_export(
                                second_chosen.loc, symbol_name_for_choice
                            )
                        if accept and fix_call:
                            accept = not _definition_location_is_call_site_ast(
                                second_chosen.path, second_chosen.loc
                            ) and not _definition_source_looks_like_usage(
                                second_chosen.loc,
                                symbol_name_for_choice,
                                ctx.doc_uri,
                                second_src or "",
                            )
                        if accept:
                            chosen_def = second_chosen
                            full_def_source = second_src
                            result["chosen_definition_reason"] = {
                                **result.get("chosen_definition_reason", {}),
                                "note": (
                                    "second_hop_from_import_to_definition"
                                    if fix_import and not fix_call
                                    else "second_hop_from_call_site_to_definition"
                                ),
                            }
            except Exception:
                pass

    upgraded_from_declaration, declaration_surface_snapshot, runtime_implementation, ext_trace = (
        _try_external_declaration_runtime_upgrade(
            client,
            ctx.repo_root,
            chosen_def,
            full_def_source,
            symbol_name_for_choice,
        )
    )
    if ext_trace is not None:
        result["chosen_definition_reason"] = {
            **(result.get("chosen_definition_reason") or {}),
            "external_runtime_resolution": ext_trace,
        }
    # After external runtime upgrade, verify symbol anchoring again.
    if (
        client is not None
        and symbol_name_for_choice
        and not _definition_source_matches_symbol(full_def_source, symbol_name_for_choice)
    ):
        try:
            syms = client.document_symbols(chosen_def.loc.uri)
            sym_loc = _find_symbol_location_from_document_symbols(
                syms,
                uri=chosen_def.loc.uri,
                symbol_name=symbol_name_for_choice,
                hint_line0=chosen_def.loc.start_line,
                parent_name_hint=receiver_parent_hint,
            )
            if sym_loc is not None:
                refined = _build_def_candidate(ctx.repo_root, sym_loc)
                refined_src = _read_definition_source(
                    refined.loc,
                    symbol_name_for_choice,
                    usage_hint=usage_hint,
                )
                if _definition_source_matches_symbol(refined_src, symbol_name_for_choice):
                    chosen_def = refined
                    full_def_source = refined_src
                    result["chosen_definition_reason"] = {
                        **(result.get("chosen_definition_reason") or {}),
                        "note": "post_upgrade_refined_via_document_symbols",
                    }
        except Exception:
            pass
        # If runtime upgrade still isn't anchored to the symbol, return the original declaration surface.
        if (
            declaration_surface_snapshot is not None
            and not _definition_source_matches_symbol(full_def_source, symbol_name_for_choice)
        ):
            try:
                ds = declaration_surface_snapshot
                ds_range = ds.get("range") or {}
                ds_start = (ds_range.get("start") or {})
                ds_end = (ds_range.get("end") or {})
                decl_loc = Location(
                    uri=str(ds.get("uri") or ""),
                    start_line=int(ds_start.get("line0", 0)),
                    start_col=int(ds_start.get("col0", 0)),
                    end_line=int(ds_end.get("line0", 0)),
                    end_col=int(ds_end.get("col0", 0)),
                )
                decl_cand = _build_def_candidate(ctx.repo_root, decl_loc)
                decl_src = _read_definition_source(
                    decl_loc, symbol_name_for_choice, usage_hint=usage_hint
                )
                if _definition_source_matches_symbol(decl_src, symbol_name_for_choice):
                    chosen_def = decl_cand
                    full_def_source = decl_src
                    result["chosen_definition_reason"] = {
                        **(result.get("chosen_definition_reason") or {}),
                        "note": "runtime_unresolved_fell_back_to_declaration",
                    }
            except Exception:
                pass

    outer = _build_outer_definition(
        chosen_def=chosen_def,
        repo_root=ctx.repo_root,
        full_def_source=full_def_source,
        client=client,
        declaration_surface=declaration_surface_snapshot if upgraded_from_declaration else None,
        runtime_implementation=runtime_implementation,
    )
    #---phase 6---- check the nested callee
    #--- edit this to be ast separated and resurvie

    nested_recs: List[Dict[str, Any]] = []
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
                                type_locs = client.goto_definition(uloc.uri, uloc.start_line, type_col)
                                if not type_locs:
                                    type_locs = client.goto_type_definition(uloc.uri, uloc.start_line, type_col)
                                if type_locs:
                                    type_loc = type_locs[0]
                                    type_src = _read_definition_source(type_loc, type_name)
                                    if type_src:
                                        full_src = type_src
                                    elif type_loc.uri != uloc.uri or type_loc.start_line != uloc.start_line:
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
    return LspDefinitionOutcome(result=result, context=ctx)
