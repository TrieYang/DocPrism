"""Heuristics for refining LSP definition hits.

Used after standard definition/implementation navigation lands on a
type/signature surface (``.d.ts``, import/re-export, call site, etc.).

Responsibilities:
- detect type/signature surfaces
- second-hop from import / call sites
- external ``.d.ts`` → runtime implementation upgrade
- document-symbol re-anchoring (and fall back to the declaration)
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from lsp_client import GenericLSPClient, Location, file_uri, uri_to_path
from models import DefCandidate, ResolutionContext
from ts_definition_ops import (
    _build_def_candidate,
    _choose_one_definition,
    _definition_location_is_call_site_ast,
    _definition_source_is_import_or_export,
    _definition_source_looks_like_usage,
    _definition_source_matches_symbol,
    _find_definition_via_imports,
    _find_symbol_location_from_document_symbols,
    _try_external_declaration_runtime_upgrade,
)


def looks_like_type_or_signature_surface(
    chosen_def: DefCandidate,
    full_def_source: Optional[str],
    symbol_name: Optional[str],
    *,
    doc_uri: Optional[str] = None,
) -> bool:
    """True when the hit looks like a type/signature, not a usable implementation body."""
    if chosen_def.is_d_ts:
        return True
    # Ambient / interface / type-only AST nodes (including when we only kept a stub).
    try:
        from ts_ast import is_type_or_signature_surface_at

        if is_type_or_signature_surface_at(
            chosen_def.path, chosen_def.loc.start_line, chosen_def.loc.start_col
        ):
            return True
    except Exception:
        pass
    if symbol_name and _definition_source_is_import_or_export(chosen_def.loc, symbol_name):
        return True
    if symbol_name and full_def_source and (
        _definition_location_is_call_site_ast(chosen_def.path, chosen_def.loc)
        or _definition_source_looks_like_usage(
            chosen_def.loc,
            symbol_name,
            doc_uri or "",
            full_def_source,
        )
    ):
        return True
    return False


def follow_non_definition_hop(
    client: GenericLSPClient,
    ctx: ResolutionContext,
    chosen_def: DefCandidate,
    full_def_source: Optional[str],
    *,
    symbol_name: Optional[str],
    usage_hint: str,
    result: Dict[str, Any],
) -> Tuple[DefCandidate, Optional[str]]:
    """If LSP landed on an import/re-export or call site, follow one hop to a definition."""
    from code_navigation_TypeScript import _read_definition_source

    fix_import = bool(
        symbol_name and _definition_source_is_import_or_export(chosen_def.loc, symbol_name)
    )
    fix_call = bool(
        symbol_name
        and full_def_source
        and (
            _definition_location_is_call_site_ast(chosen_def.path, chosen_def.loc)
            or _definition_source_looks_like_usage(
                chosen_def.loc,
                symbol_name,
                ctx.doc_uri,
                full_def_source,
            )
        )
    )
    if not (fix_import or fix_call):
        return chosen_def, full_def_source

    prefer_same_doc_uri = ctx.prefer_same_document_uri

    if fix_call:
        found = _find_definition_via_imports(ctx.file_path, symbol_name, ctx.repo_root)
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
                loc_found, symbol_name, usage_hint=usage_hint
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
                        symbol_name,
                        ctx.doc_uri,
                        full_def_source,
                    )
                )

    fix_import = bool(
        symbol_name and _definition_source_is_import_or_export(chosen_def.loc, symbol_name)
    )
    if not (fix_import or fix_call):
        return chosen_def, full_def_source

    try:
        second_locs = client.goto_definition(
            chosen_def.loc.uri,
            chosen_def.loc.start_line,
            chosen_def.loc.start_col,
        )
        if not second_locs:
            return chosen_def, full_def_source

        if fix_call:
            second_candidates_with_def = [
                loc
                for loc in second_locs
                if not _definition_location_is_call_site_ast(uri_to_path(loc.uri), loc)
                and not _definition_source_looks_like_usage(
                    loc,
                    symbol_name,
                    ctx.doc_uri,
                    _read_definition_source(loc, symbol_name, usage_hint=usage_hint),
                )
            ]
            pool = second_candidates_with_def if second_candidates_with_def else second_locs
        else:
            pool = second_locs

        second_chosen, _ = _choose_one_definition(
            ctx.repo_root,
            pool,
            symbol_name=symbol_name,
            usage_kind=ctx.selector.kind,
            prefer_same_document_uri=prefer_same_doc_uri,
        )
        if second_chosen is None:
            return chosen_def, full_def_source

        second_src = _read_definition_source(
            second_chosen.loc, symbol_name, usage_hint=usage_hint
        )
        accept = bool(second_src)
        if accept and fix_import:
            accept = not _definition_source_is_import_or_export(
                second_chosen.loc, symbol_name
            )
        if accept and fix_call:
            accept = not _definition_location_is_call_site_ast(
                second_chosen.path, second_chosen.loc
            ) and not _definition_source_looks_like_usage(
                second_chosen.loc,
                symbol_name,
                ctx.doc_uri,
                second_src or "",
            )
        if accept:
            result["chosen_definition_reason"] = {
                **result.get("chosen_definition_reason", {}),
                "note": (
                    "second_hop_from_import_to_definition"
                    if fix_import and not fix_call
                    else "second_hop_from_call_site_to_definition"
                ),
            }
            return second_chosen, second_src
    except Exception:
        pass

    return chosen_def, full_def_source


def refine_type_surface_to_implementation(
    client: Optional[GenericLSPClient],
    ctx: ResolutionContext,
    chosen_def: DefCandidate,
    full_def_source: Optional[str],
    *,
    symbol_name: Optional[str],
    usage_hint: str,
    receiver_parent_hint: Optional[str],
    result: Dict[str, Any],
) -> Tuple[DefCandidate, Optional[str], Optional[Dict[str, Any]], Optional[Dict[str, Any]], bool]:
    """
    Try to turn a type/signature hit into a runtime implementation.

    Returns
    ``(chosen_def, full_def_source, declaration_surface, runtime_implementation, upgraded)``.
    Keeps the original stub/type text; if upgrade/re-anchor fails, that stub is
    what the caller finishes with.
    """
    from code_navigation_TypeScript import _read_definition_source

    # (1) Keep whatever stub/type text we already have.
    stub_def = chosen_def
    stub_source = full_def_source

    upgraded, declaration_surface, runtime_implementation, ext_trace = (
        _try_external_declaration_runtime_upgrade(
            client,
            ctx.repo_root,
            chosen_def,
            full_def_source,
            symbol_name,
        )
    )
    if ext_trace is not None:
        result["chosen_definition_reason"] = {
            **(result.get("chosen_definition_reason") or {}),
            "external_runtime_resolution": ext_trace,
            "note": "type_or_signature_surface_tried_heuristics",
        }
    else:
        result["chosen_definition_reason"] = {
            **(result.get("chosen_definition_reason") or {}),
            "note": "type_or_signature_surface_kept_stub",
            "type_or_signature_surface": True,
        }

    if (
        client is not None
        and symbol_name
        and not _definition_source_matches_symbol(full_def_source, symbol_name)
    ):
        try:
            syms = client.document_symbols(chosen_def.loc.uri)
            sym_loc = _find_symbol_location_from_document_symbols(
                syms,
                uri=chosen_def.loc.uri,
                symbol_name=symbol_name,
                hint_line0=chosen_def.loc.start_line,
                parent_name_hint=receiver_parent_hint,
            )
            if sym_loc is not None:
                refined = _build_def_candidate(ctx.repo_root, sym_loc)
                refined_src = _read_definition_source(
                    refined.loc,
                    symbol_name,
                    usage_hint=usage_hint,
                )
                if _definition_source_matches_symbol(refined_src, symbol_name):
                    chosen_def = refined
                    full_def_source = refined_src
                    result["chosen_definition_reason"] = {
                        **(result.get("chosen_definition_reason") or {}),
                        "note": "post_upgrade_refined_via_document_symbols",
                    }
        except Exception:
            pass

        if (
            declaration_surface is not None
            and not _definition_source_matches_symbol(full_def_source, symbol_name)
        ):
            try:
                ds = declaration_surface
                ds_range = ds.get("range") or {}
                ds_start = ds_range.get("start") or {}
                ds_end = ds_range.get("end") or {}
                decl_loc = Location(
                    uri=str(ds.get("uri") or ""),
                    start_line=int(ds_start.get("line0", 0)),
                    start_col=int(ds_start.get("col0", 0)),
                    end_line=int(ds_end.get("line0", 0)),
                    end_col=int(ds_end.get("col0", 0)),
                )
                decl_cand = _build_def_candidate(ctx.repo_root, decl_loc)
                decl_src = _read_definition_source(
                    decl_loc, symbol_name, usage_hint=usage_hint
                )
                if _definition_source_matches_symbol(decl_src, symbol_name):
                    chosen_def = decl_cand
                    full_def_source = decl_src
                    result["chosen_definition_reason"] = {
                        **(result.get("chosen_definition_reason") or {}),
                        "note": "runtime_unresolved_fell_back_to_declaration",
                    }
            except Exception:
                pass

    # (3) If heuristics did not produce a better body, return the kept stub.
    if not _definition_source_matches_symbol(full_def_source, symbol_name or ""):
        chosen_def = stub_def
        full_def_source = stub_source
    elif full_def_source is None and stub_source is not None:
        chosen_def = stub_def
        full_def_source = stub_source

    return (
        chosen_def,
        full_def_source,
        declaration_surface,
        runtime_implementation,
        upgraded,
    )


def reanchor_if_symbol_mismatch(
    client: GenericLSPClient,
    chosen_def: DefCandidate,
    full_def_source: Optional[str],
    *,
    repo_root,
    symbol_name: Optional[str],
    receiver_parent_hint: Optional[str],
) -> Tuple[DefCandidate, Optional[str], bool, bool]:
    """
    Light re-anchor used on the goToSourceDefinition success path.

    Returns ``(chosen, source, ok, did_refine)``. ``ok`` is False when the
    source still does not mention ``symbol_name`` (caller should treat step 1
    as a miss).
    """
    from code_navigation_TypeScript import _read_definition_source

    if not symbol_name or _definition_source_matches_symbol(full_def_source, symbol_name):
        return chosen_def, full_def_source, True, False

    try:
        syms = client.document_symbols(chosen_def.loc.uri)
        sym_loc = _find_symbol_location_from_document_symbols(
            syms,
            uri=chosen_def.loc.uri,
            symbol_name=symbol_name,
            hint_line0=chosen_def.loc.start_line,
            parent_name_hint=receiver_parent_hint,
        )
        if sym_loc is not None:
            refined = _build_def_candidate(repo_root, sym_loc)
            refined_src = _read_definition_source(refined.loc, symbol_name)
            if _definition_source_matches_symbol(refined_src, symbol_name):
                return refined, refined_src, True, True
    except Exception:
        pass

    return chosen_def, full_def_source, False, False
