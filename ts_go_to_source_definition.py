"""Phase 3: resolve via TypeScript ``goToSourceDefinition``.

Given a prepared + located ResolutionContext, ask the LSP for source
definitions at the navigation cursor. On a usable hit, finish the result
(``ok=True``). On miss/skip, leave the result unfinished and keep any LSP
client on ``ctx.client`` for later strategies.

Depends on models + ts_lsp + ts_definition_ops. Snippet extraction still
lives in code_navigation_TypeScript and is imported lazily to avoid cycles.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

from models import ResolutionContext, build_success_result
from ts_definition_ops import (
    _build_def_candidate,
    _build_outer_definition,
    _choose_one_definition,
    _definition_source_matches_symbol,
    _find_symbol_location_from_document_symbols,
    _prefer_lib_global_constructor_snippet,
    _try_external_declaration_runtime_upgrade,
)
from ts_lsp import get_or_create_ts_lsp_client


@dataclass(frozen=True)
class SourceDefinitionOutcome:
    """Phase-3 result.

    ``resolved`` means phase 3 produced a finished successful result and the
    caller should return it. Otherwise later phases should continue; ``context``
    may still carry a warm LSP ``client``.
    """

    result: Dict[str, Any]
    context: ResolutionContext
    resolved: bool = False

    @property
    def ok(self) -> bool:
        return self.resolved


def try_go_to_source_definition(
    ctx: ResolutionContext,
    result: Dict[str, Any],
) -> SourceDefinitionOutcome:
    """Run phase 3: primary resolution via goToSourceDefinition."""
    if not ctx.go_to_source_definition:
        return SourceDefinitionOutcome(result=result, context=ctx, resolved=False)

    # Lazy import: snippet extraction still owned by the monolith.
    from code_navigation_TypeScript import _read_definition_source

    nav = ctx.navigation
    client = ctx.client
    try:
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
        time.sleep(0.15)
        source_def_locs = client.goto_source_definition(
            ctx.doc_uri, nav.line0, nav.col0
        )
    except Exception:
        ctx.client = client
        return SourceDefinitionOutcome(result=result, context=ctx, resolved=False)

    ctx.client = client
    if not source_def_locs:
        return SourceDefinitionOutcome(result=result, context=ctx, resolved=False)

    locs_json = [loc.to_json() for loc in source_def_locs]
    result["source_definition_locations"] = locs_json
    result["definitions_all"] = locs_json
    result["definitions_all_filtered"] = locs_json

    symbol_name = ctx.symbol_name
    receiver_parent_hint: Optional[str] = None
    if ctx.selector.receiver:
        receiver_parent_hint = ctx.selector.receiver.split(".")[-1].strip() or None

    chosen_def, debug = _choose_one_definition(
        ctx.repo_root,
        source_def_locs,
        symbol_name=symbol_name,
        usage_kind=ctx.selector.kind,
        prefer_same_document_uri=ctx.prefer_same_document_uri,
        preferred_locations=source_def_locs,
    )
    if chosen_def is None:
        return SourceDefinitionOutcome(result=result, context=ctx, resolved=False)

    full_def_source = _read_definition_source(chosen_def.loc, symbol_name)
    full_def_source = _prefer_lib_global_constructor_snippet(
        full_def_source,
        chosen_def.path,
        symbol_name,
        usage_kind=ctx.selector.kind,
    )

    upgraded, declaration_surface, runtime_implementation, ext_trace = (
        _try_external_declaration_runtime_upgrade(
            client,
            ctx.repo_root,
            chosen_def,
            full_def_source,
            symbol_name,
        )
    )
    if upgraded and ext_trace is not None:
        debug = {**debug, "external_runtime_resolution": ext_trace}
    elif chosen_def.is_d_ts and chosen_def.in_node_modules:
        return SourceDefinitionOutcome(result=result, context=ctx, resolved=False)

    if symbol_name and not _definition_source_matches_symbol(full_def_source, symbol_name):
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
                refined_src = _read_definition_source(refined.loc, symbol_name)
                if _definition_source_matches_symbol(refined_src, symbol_name):
                    chosen_def = refined
                    full_def_source = refined_src
                    debug = {**debug, "note": "primary_refined_via_document_symbols"}
        except Exception:
            pass
        if not _definition_source_matches_symbol(full_def_source, symbol_name):
            return SourceDefinitionOutcome(result=result, context=ctx, resolved=False)

    outer = _build_outer_definition(
        chosen_def=chosen_def,
        repo_root=ctx.repo_root,
        full_def_source=full_def_source,
        client=client,
        declaration_surface=declaration_surface if upgraded else None,
        runtime_implementation=runtime_implementation,
    )

    result["chosen_definition_reason"] = {
        **debug,
        "note": "go_to_source_definition_primary",
        "go_to_source_definition": True,
    }
    result["definitions"] = [
        {
            "outer_ok": True,
            "outer_error": None,
            "outer_definition": outer,
            "argument_usages_resolved": [],
        }
    ]
    build_success_result(result)
    return SourceDefinitionOutcome(result=result, context=ctx, resolved=True)
