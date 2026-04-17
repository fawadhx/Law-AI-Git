from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.legal_corpus import (
    IngestionRunRecord,
    IngestionSourceDefinition,
    LegalCorpusSourcePreview,
    NormalizedInstrumentBundle,
    ReviewFieldDescriptor,
)
from app.services.legal_corpus_store import record_ingestion_run, upsert_instrument_bundle
from app.services.legal_ingestion import get_ingestion_source_registry, get_seed_source_documents
from app.services.legal_ingestion.normalization import normalize_source_document


def list_available_ingestion_sources() -> list[IngestionSourceDefinition]:
    return get_ingestion_source_registry()


def get_admin_review_fields() -> list[ReviewFieldDescriptor]:
    return [
        ReviewFieldDescriptor(key="title", label="Title", description="Official long title of the instrument."),
        ReviewFieldDescriptor(key="short_title", label="Short title", description="Common short title where available.", required=False),
        ReviewFieldDescriptor(key="jurisdiction", label="Jurisdiction", description="Jurisdiction covered by the law."),
        ReviewFieldDescriptor(key="government_level", label="Government level", description="Federal now, provincial later."),
        ReviewFieldDescriptor(key="category", label="Category", description="Topical category such as criminal law or labor."),
        ReviewFieldDescriptor(key="law_type", label="Law type", description="Act, Ordinance, Rule, Regulation, SRO, or related instrument type."),
        ReviewFieldDescriptor(key="promulgation_date", label="Promulgation date", description="Date the law was promulgated.", required=False),
        ReviewFieldDescriptor(key="effective_date", label="Effective date", description="In-force date where available.", required=False),
        ReviewFieldDescriptor(key="status", label="Status", description="Active, repealed, amended, under review, or unknown."),
        ReviewFieldDescriptor(key="official_citation", label="Official citation", description="Official citation or act number where available.", required=False),
        ReviewFieldDescriptor(key="source_url", label="Source URL", description="Exact official source used for ingestion."),
        ReviewFieldDescriptor(key="gazette_reference", label="Gazette reference", description="Gazette issue or notification reference.", required=False),
        ReviewFieldDescriptor(key="language", label="Language", description="Source language code."),
        ReviewFieldDescriptor(key="version_label", label="Version label", description="Repository or Gazette version label.", required=False),
        ReviewFieldDescriptor(key="amendment_notes", label="Amendment notes", description="Amendment or revision notes if provided.", required=False),
        ReviewFieldDescriptor(key="source_trust_level", label="Trust level", description="Gazette original, official repository, or fallback tier."),
    ]


def preview_seed_documents() -> list[LegalCorpusSourcePreview]:
    previews: list[LegalCorpusSourcePreview] = []
    source_label_map = {source.source_slug: source.label for source in get_ingestion_source_registry()}
    for document in get_seed_source_documents():
        previews.append(
            LegalCorpusSourcePreview(
                source_slug=document.source_slug,
                source_label=source_label_map.get(document.source_slug, document.source_slug),
                trust_level=document.source_trust_level,
                sample_document_title=document.title,
                source_url=document.source_url,
                official_citation=document.official_citation,
                gazette_reference=document.gazette_reference,
                law_type=document.law_type,
                category=document.category,
                government_level=document.government_level,
                promulgation_date=document.promulgation_date,
                effective_date=document.effective_date,
                status=document.status,
                language=document.language,
                provenance_summary=(
                    f"{source_label_map.get(document.source_slug, document.source_slug)} seed document from an official federal source."
                ),
                extraction_notes=[
                    str(document.extraction_metadata.get("seed_reason", "Seeded for adapter validation.")),
                    "This preview is metadata-only and does not publish text into retrieval.",
                ],
            )
        )
    return previews


def plan_federal_bootstrap_runs() -> list[IngestionRunRecord]:
    planned_at = datetime.now(timezone.utc).isoformat()
    runs: list[IngestionRunRecord] = []

    for source in get_ingestion_source_registry():
        if source.government_level != "federal" or not source.active:
            continue
        runs.append(
            IngestionRunRecord(
                run_id=f"planned-{source.source_slug}-{uuid4().hex[:8]}",
                adapter_key=source.source_slug,
                scope_label="pakistan_federal_bootstrap",
                jurisdiction=source.jurisdiction,
                government_level=source.government_level,
                status="planned",
                run_metadata={
                    "planned_at": planned_at,
                    "mode": "bootstrap",
                    "review_gate": "admin_review_required_before_publish",
                    "notes": [
                        "No automated source fetch is executed in this scaffold.",
                        "Adapters are ready for official-source discovery, normalization, and dedup integration.",
                    ],
                },
            )
        )

    return runs


def bootstrap_federal_seed_metadata() -> dict[str, object]:
    normalized_bundles: list[NormalizedInstrumentBundle] = [
        normalize_source_document(document) for document in get_seed_source_documents()
    ]
    persisted = 0
    runs = plan_federal_bootstrap_runs()

    for run in runs:
        if record_ingestion_run(run):
            persisted += 1

    bundle_persisted = 0
    for bundle in normalized_bundles:
        if upsert_instrument_bundle(bundle):
            bundle_persisted += 1

    return {
        "planned_run_count": len(runs),
        "recorded_run_count": persisted,
        "normalized_bundle_count": len(normalized_bundles),
        "persisted_bundle_count": bundle_persisted,
    }
