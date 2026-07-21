"""Primary definition resolution via LSP (replaces old phases 3–5).

Flow:
1. ``goToSourceDefinition`` — if a usable (non-type) hit, finish successfully.
2. ``definition`` / ``implementation`` (+ ``typeDefinition`` fallback) —
   if the hit is not a type/signature surface, take it.
3. Otherwise run heuristics (second hop, ``.d.ts`` → runtime, re-anchor).
   If heuristics fail, keep the type/signature from step 2.

On a successful standard-LSP path, returns a ``PrimaryDefinition`` for nested
usage resolution. On goToSourceDefinition success or hard failure, ``done``
is True and the caller should return ``result`` immediately.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from models import PrimaryDefinition, ResolutionContext, build_failure_result, build_success_result
from ts_definition_heuristics import (
    follow_non_definition_hop,
    looks_like_type_or_signature_surface,
    reanchor_if_symbol_mismatch,
    refine_type_surface_to_implementation,
)
from ts_definition_ops import (
    _build_outer_definition,
    _choose_one_definition,
    _dedupe_locations,
    _extract_function_range_from_symbols,
)
from ts_lsp import get_or_create_ts_lsp_client


@dataclass(frozen=True)
class PrimaryResolveOutcome:
    """Result of primary (pre-nested) resolution."""

    result: Dict[str, Any]
    context: ResolutionContext
    # When set and ``done`` is False, caller should run nested usages next.
    primary: Optional[PrimaryDefinition] = None
    # True → caller returns ``result`` now (success via source-def, or failure).
    done: bool = False


def _receiver_parent_hint(ctx: ResolutionContext) -> Optional[str]:
    if ctx.selector.receiver:
        return ctx.selector.receiver.split(".")[-1].strip() or None
    return None


def _ensure_client(ctx: ResolutionContext, *, sleep_s: float = 0.15) -> Any:
    client = ctx.client
    if client is None:
        client = get_or_create_ts_lsp_client(
            ctx.repo_root,
            ctx.file_path,
            ctx.lang_id,
            ctx.cmd,
            ctx.root_uri,
            ctx.workspace_uris,
        )
        ctx.client = client
    client.open_document(ctx.doc_uri, ctx.text)
    time.sleep(sleep_s)
    return client


def _fetch_standard_definition_locations(client: Any, ctx: ResolutionContext) -> List[Any]:
    nav = ctx.navigation
    if ctx.selector.kind == "attr":
        locs: List[Any] = []
        locs.extend(client.goto_definition(ctx.doc_uri, nav.line0, nav.col0))
        locs.extend(client.goto_type_definition(ctx.doc_uri, nav.line0, nav.col0))
        locs.extend(client.goto_implementation(ctx.doc_uri, nav.line0, nav.col0))
        return _dedupe_locations(locs)

    locs = []
    locs.extend(client.goto_implementation(ctx.doc_uri, nav.line0, nav.col0))
    if not locs:
        locs.extend(client.goto_definition(ctx.doc_uri, nav.line0, nav.col0))
    if not locs:
        locs = client.goto_type_definition(ctx.doc_uri, nav.line0, nav.col0)
    return _dedupe_locations(locs)


def _finish_source_definition_success(
    ctx: ResolutionContext,
    result: Dict[str, Any],
    *,
    chosen_def,
    full_def_source: Optional[str],
    debug: Dict[str, Any],
    client: Any,
) -> PrimaryResolveOutcome:
    outer = _build_outer_definition(
        chosen_def=chosen_def,
        repo_root=ctx.repo_root,
        full_def_source=full_def_source,
        client=client,
    )
    result["chosen_definition_reason"] = {
        **debug,
        "note": "go_to_source_definition_primary",
        "go_to_source_definition": True,
    }
    result["resolution_path"] = "source_definition"
    result["definitions"] = [
        {
            "outer_ok": True,
            "outer_error": None,
            "outer_definition": outer,
            "argument_usages_resolved": [],
        }
    ]
    build_success_result(result)
    return PrimaryResolveOutcome(result=result, context=ctx, done=True)


def _build_primary_for_nested(
    ctx: ResolutionContext,
    result: Dict[str, Any],
    *,
    chosen_def,
    full_def_source: Optional[str],
    symbol_name: Optional[str],
    usage_hint: str,
    receiver_parent_hint: Optional[str],
    client: Any,
    declaration_surface: Optional[Dict[str, Any]] = None,
    runtime_implementation: Optional[Dict[str, Any]] = None,
    upgraded: bool = False,
) -> PrimaryDefinition:
    outer = _build_outer_definition(
        chosen_def=chosen_def,
        repo_root=ctx.repo_root,
        full_def_source=full_def_source,
        client=client,
        declaration_surface=declaration_surface if upgraded else None,
        runtime_implementation=runtime_implementation,
    )
    outer_item: Dict[str, Any] = {
        "outer_ok": False,
        "outer_error": None,
        "outer_definition": None,
        "argument_usages_resolved": [],
    }
    return PrimaryDefinition(
        chosen_def=chosen_def,
        full_def_source=full_def_source,
        symbol_name=symbol_name,
        receiver_parent_hint=receiver_parent_hint,
        usage_hint=usage_hint,
        declaration_surface=declaration_surface,
        runtime_implementation=runtime_implementation,
        upgraded_from_declaration=upgraded,
        outer_definition=outer,
        outer_item=outer_item,
    )


def resolve_primary_definition(
    ctx: ResolutionContext,
    result: Dict[str, Any],
) -> PrimaryResolveOutcome:
    """Run primary resolution steps 1–3."""
    from code_navigation_TypeScript import _read_definition_source

    symbol_name = ctx.symbol_name
    usage_hint = ctx.search_text
    receiver_parent_hint = _receiver_parent_hint(ctx)
    client = ctx.client

    # --- Step 1: goToSourceDefinition ---
    if ctx.go_to_source_definition:
        try:
            client = _ensure_client(ctx, sleep_s=0.15)
            source_def_locs = client.goto_source_definition(
                ctx.doc_uri, ctx.navigation.line0, ctx.navigation.col0
            )
        except Exception:
            ctx.client = client
            source_def_locs = []

        ctx.client = client
        if source_def_locs:
            locs_json = [loc.to_json() for loc in source_def_locs]
            result["source_definition_locations"] = locs_json
            result["definitions_all"] = locs_json
            result["definitions_all_filtered"] = locs_json

            chosen_def, debug = _choose_one_definition(
                ctx.repo_root,
                source_def_locs,
                symbol_name=symbol_name,
                usage_kind=ctx.selector.kind,
                prefer_same_document_uri=ctx.prefer_same_document_uri,
                preferred_locations=source_def_locs,
            )
            if chosen_def is not None:
                full_def_source = _read_definition_source(chosen_def.loc, symbol_name)
                # Type/signature from source-def → fall through to step 2.
                if not looks_like_type_or_signature_surface(
                    chosen_def,
                    full_def_source,
                    symbol_name,
                    doc_uri=ctx.doc_uri,
                ):
                    chosen_def, full_def_source, ok, did_refine = reanchor_if_symbol_mismatch(
                        client,
                        chosen_def,
                        full_def_source,
                        repo_root=ctx.repo_root,
                        symbol_name=symbol_name,
                        receiver_parent_hint=receiver_parent_hint,
                    )
                    if ok:
                        if did_refine:
                            debug = {**debug, "note": "primary_refined_via_document_symbols"}
                        return _finish_source_definition_success(
                            ctx,
                            result,
                            chosen_def=chosen_def,
                            full_def_source=full_def_source,
                            debug=debug,
                            client=client,
                        )

    # --- Step 2: standard definition / implementation ---
    outer_item_fail: Dict[str, Any] = {
        "outer_ok": False,
        "outer_error": None,
        "outer_definition": None,
        "argument_usages_resolved": [],
    }
    try:
        if client is None:
            client = _ensure_client(ctx, sleep_s=0.2)
            if ctx.expr_rng is None:
                try:
                    symbols = client.document_symbols(ctx.doc_uri)
                    sym_rng = _extract_function_range_from_symbols(
                        symbols, ctx.tested_function
                    )
                    if sym_rng is not None:
                        ctx.expr_rng = sym_rng
                except Exception:
                    pass
        else:
            # Client may already be warm from step 1.
            pass

        locs = _fetch_standard_definition_locations(client, ctx)
    except Exception as e:
        result["resolution_path"] = "failed"
        return PrimaryResolveOutcome(
            result=build_failure_result(
                result, error=f"LSP definition request failed: {e}"
            ),
            context=ctx,
            done=True,
        )

    result["definitions_all"] = [loc.to_json() for loc in locs]
    result["definitions_all_filtered"] = [loc.to_json() for loc in locs]

    if not locs:
        outer_item_fail["outer_error"] = "No definition found from TypeScript LSP."
        result["definitions"] = [outer_item_fail]
        result["resolution_path"] = "failed"
        return PrimaryResolveOutcome(
            result=build_failure_result(result, error=outer_item_fail["outer_error"]),
            context=ctx,
            done=True,
        )

    chosen_def, debug = _choose_one_definition(
        ctx.repo_root,
        locs,
        symbol_name=symbol_name,
        usage_kind=ctx.selector.kind,
        prefer_same_document_uri=ctx.prefer_same_document_uri,
    )
    result["chosen_definition_reason"] = debug

    if chosen_def is None:
        outer_item_fail["outer_error"] = "No valid implementation found after filtering."
        result["definitions"] = [outer_item_fail]
        result["resolution_path"] = "failed"
        return PrimaryResolveOutcome(
            result=build_failure_result(result, error=outer_item_fail["outer_error"]),
            context=ctx,
            done=True,
        )

    full_def_source = _read_definition_source(
        chosen_def.loc, symbol_name, usage_hint=usage_hint
    )

    # Heuristic: leave import/call sites via a second hop before classifying.
    reason_before_hop = dict(result.get("chosen_definition_reason") or {})
    chosen_def, full_def_source = follow_non_definition_hop(
        client,
        ctx,
        chosen_def,
        full_def_source,
        symbol_name=symbol_name,
        usage_hint=usage_hint,
        result=result,
    )
    hop_note = str((result.get("chosen_definition_reason") or {}).get("note") or "")
    used_hop_heuristic = hop_note != str(reason_before_hop.get("note") or "")

    declaration_surface = None
    runtime_implementation = None
    upgraded = False
    used_type_heuristics = False

    # --- Step 3: if type/signature, try heuristics; else keep as-is ---
    if looks_like_type_or_signature_surface(
        chosen_def,
        full_def_source,
        symbol_name,
        doc_uri=ctx.doc_uri,
    ):
        used_type_heuristics = True
        (
            chosen_def,
            full_def_source,
            declaration_surface,
            runtime_implementation,
            upgraded,
        ) = refine_type_surface_to_implementation(
            client,
            ctx,
            chosen_def,
            full_def_source,
            symbol_name=symbol_name,
            usage_hint=usage_hint,
            receiver_parent_hint=receiver_parent_hint,
            result=result,
        )

    if used_type_heuristics or used_hop_heuristic:
        result["resolution_path"] = "heuristics"
    else:
        result["resolution_path"] = "definition_or_implementation"

    primary = _build_primary_for_nested(
        ctx,
        result,
        chosen_def=chosen_def,
        full_def_source=full_def_source,
        symbol_name=symbol_name,
        usage_hint=usage_hint,
        receiver_parent_hint=receiver_parent_hint,
        client=client,
        declaration_surface=declaration_surface,
        runtime_implementation=runtime_implementation,
        upgraded=upgraded,
    )
    return PrimaryResolveOutcome(
        result=result, context=ctx, primary=primary, done=False
    )
