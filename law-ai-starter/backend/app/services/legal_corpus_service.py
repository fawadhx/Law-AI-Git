from __future__ import annotations

from datetime import datetime, timezone

from app.schemas.legal_corpus import (
    LegalCorpusFoundationResponse,
    LegalCorpusInstrumentCatalogResponse,
    LegalCorpusLayerInfo,
)
from app.services.legal_corpus_store import get_legal_corpus_storage_snapshot, list_corpus_instruments
from app.services.legal_import_service import (
    get_admin_review_fields,
    plan_federal_bootstrap_runs,
    preview_seed_documents,
)
from app.services.legal_ingestion import get_ingestion_bootstrap_notes, get_ingestion_source_registry


def get_legal_corpus_foundation() -> LegalCorpusFoundationResponse:
    storage = get_legal_corpus_storage_snapshot()
    notes = [
        "This milestone adds canonical corpus tables for instrument, version, provision, and ingestion-run tracking without replacing the existing prototype legal_source_records flow.",
        "Imported official-source content should stay unpublished until admin review maps it into a reviewed version and, later, retrieval-ready provision records.",
        "Federal Pakistan Code and Gazette-backed ingestion adapters are scaffolded first; provincial repositories should plug into the same adapter contract in a later phase.",
    ]
    notes.extend(get_ingestion_bootstrap_notes())

    return LegalCorpusFoundationResponse(
        generated_at=datetime.now(timezone.utc).isoformat(),
        storage=storage,
        canonical_layers=[
            LegalCorpusLayerInfo(
                layer="instrument",
                storage_target="legal_instruments",
                purpose="Canonical law-level identity and metadata for an Act, Ordinance, Rule, Regulation, or notification family.",
            ),
            LegalCorpusLayerInfo(
                layer="version",
                storage_target="legal_instrument_versions",
                purpose="Immutable sourced document versions with provenance, raw text, cleaned text, Gazette references, and review state.",
            ),
            LegalCorpusLayerInfo(
                layer="provision",
                storage_target="legal_provisions",
                purpose="Structured sections and subsections extracted from a reviewed version and prepared for future retrieval indexing.",
            ),
            LegalCorpusLayerInfo(
                layer="ingestion_run",
                storage_target="ingestion_runs",
                purpose="Operational audit trail for imports, sync runs, duplicate detection, and source-adapter diagnostics.",
            ),
        ],
        source_registry=get_ingestion_source_registry(),
        review_fields=get_admin_review_fields(),
        source_previews=preview_seed_documents(),
        planned_runs=plan_federal_bootstrap_runs(),
        implementation_notes=notes,
    )


def get_legal_corpus_instrument_catalog() -> LegalCorpusInstrumentCatalogResponse:
    items = list_corpus_instruments()
    return LegalCorpusInstrumentCatalogResponse(
        total_records=len(items),
        items=items,
        workflow_note=(
            "These are canonical corpus-level instrument records intended for ingestion review and version tracking. "
            "They do not automatically participate in chat retrieval until later retrieval-integration phases."
        ),
    )
