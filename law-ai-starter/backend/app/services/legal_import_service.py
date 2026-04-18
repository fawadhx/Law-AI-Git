from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4

from app.core.errors import AppServiceError
from app.schemas.legal_corpus import (
    FederalImportPipelineResponse,
    IngestionDuplicateCandidate,
    IngestionImportItemResult,
    IngestionRunRecord,
    IngestionSourceDefinition,
    LegalCorpusSyncPlanResponse,
    LegalCorpusSourcePreview,
    LegalInstrumentRecord,
    NormalizedInstrumentBundle,
    ReviewFieldDescriptor,
)
from app.services.legal_corpus_store import (
    find_matching_instrument_candidates,
    find_matching_version_candidates,
    instrument_exists,
    record_ingestion_run,
    upsert_instrument_bundle,
)
from app.services.legal_ingestion import (
    get_ingestion_sync_plans,
    get_ingestion_source_registry,
    get_seed_source_documents,
    run_seed_discovery,
    run_seed_normalization,
)
from app.services.legal_ingestion.normalization import normalize_source_document


def _get_seed_documents_or_raise() -> list:
    documents = get_seed_source_documents()
    if not documents:
        raise AppServiceError(
            "No official-source seed documents are configured for this ingestion run yet.",
            status_code=503,
            error_code="ingestion_seed_unavailable",
        )
    return documents


def list_available_ingestion_sources() -> list[IngestionSourceDefinition]:
    return get_ingestion_source_registry()


def get_admin_review_fields() -> list[ReviewFieldDescriptor]:
    return [
        ReviewFieldDescriptor(key="title", label="Title", description="Official long title of the instrument."),
        ReviewFieldDescriptor(key="short_title", label="Short title", description="Common short title where available.", required=False),
        ReviewFieldDescriptor(key="jurisdiction", label="Jurisdiction", description="Jurisdiction covered by the law."),
        ReviewFieldDescriptor(key="government_level", label="Government level", description="Federal now, provincial later."),
        ReviewFieldDescriptor(key="province", label="Province", description="Province for provincial laws where applicable.", required=False),
        ReviewFieldDescriptor(key="category", label="Category", description="Topical category such as criminal law or labor."),
        ReviewFieldDescriptor(key="law_type", label="Law type", description="Act, Ordinance, Rule, Regulation, SRO, or related instrument type."),
        ReviewFieldDescriptor(key="promulgation_date", label="Promulgation date", description="Date the law was promulgated.", required=False),
        ReviewFieldDescriptor(key="effective_date", label="Effective date", description="In-force date where available.", required=False),
        ReviewFieldDescriptor(key="status", label="Status", description="Active, repealed, amended, under review, or unknown."),
        ReviewFieldDescriptor(key="official_citation", label="Official citation", description="Official citation or act number where available.", required=False),
        ReviewFieldDescriptor(key="source_url", label="Source URL", description="Exact official source used for ingestion."),
        ReviewFieldDescriptor(key="source_authority", label="Source authority", description="Official authority or repository behind the source."),
        ReviewFieldDescriptor(key="gazette_reference", label="Gazette reference", description="Gazette issue or notification reference.", required=False),
        ReviewFieldDescriptor(key="language", label="Language", description="Source language code."),
        ReviewFieldDescriptor(key="version_label", label="Version label", description="Repository or Gazette version label.", required=False),
        ReviewFieldDescriptor(key="amendment_notes", label="Amendment notes", description="Amendment or revision notes if provided.", required=False),
        ReviewFieldDescriptor(key="source_trust_level", label="Trust level", description="Gazette original, official repository, or fallback tier."),
    ]


def preview_seed_documents() -> list[LegalCorpusSourcePreview]:
    previews: list[LegalCorpusSourcePreview] = []
    source_label_map = {source.source_slug: source.label for source in get_ingestion_source_registry()}
    for document in _get_seed_documents_or_raise():
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
                    f"{source_label_map.get(document.source_slug, document.source_slug)} seed document from an official "
                    f"{document.government_level} source."
                ),
                extraction_notes=[
                    str(document.extraction_metadata.get("seed_reason", "Seeded for adapter validation.")),
                    f"Source authority: {document.source_authority or 'not set'}.",
                    "This preview is metadata-only and does not publish text into retrieval.",
                ],
            )
        )
    return previews


def plan_bootstrap_runs(
    *,
    government_level: str | None = None,
    province: str | None = None,
) -> list[IngestionRunRecord]:
    planned_at = datetime.now(timezone.utc).isoformat()
    runs: list[IngestionRunRecord] = []

    for source in get_ingestion_source_registry(government_level=government_level, province=province):
        if not source.active:
            continue
        scope_label = (
            f"pakistan_{(source.province or source.government_level).lower().replace(' ', '_')}_bootstrap"
            if source.government_level == "provincial"
            else "pakistan_federal_bootstrap"
        )
        runs.append(
            IngestionRunRecord(
                run_id=f"planned-{source.source_slug}-{uuid4().hex[:8]}",
                adapter_key=source.source_slug,
                scope_label=scope_label,
                jurisdiction=source.jurisdiction,
                government_level=source.government_level,
                status="planned",
                run_metadata={
                    "planned_at": planned_at,
                    "mode": "bootstrap",
                    "province": source.province,
                    "review_gate": "admin_review_required_before_publish",
                    "notes": [
                        "No automated source fetch is executed in this scaffold.",
                        "Adapters are ready for official-source discovery, normalization, and dedup integration.",
                    ],
                },
            )
        )

    return runs


def plan_federal_bootstrap_runs() -> list[IngestionRunRecord]:
    return plan_bootstrap_runs(government_level="federal")


def plan_provincial_bootstrap_runs() -> list[IngestionRunRecord]:
    return plan_bootstrap_runs(government_level="provincial")


def get_corpus_sync_plan() -> LegalCorpusSyncPlanResponse:
    return LegalCorpusSyncPlanResponse(
        generated_at=datetime.now(timezone.utc).isoformat(),
        sync_plans=list(get_ingestion_sync_plans()),
        workflow_note=(
            "Sync plans define how each official source should be refreshed later without assuming unsupported scraping. "
            "They preserve province and government-level separation, keep provenance mandatory, and use duplicate checks before any new version is stored."
        ),
    )


def bootstrap_federal_seed_metadata() -> dict[str, object]:
    seed_documents = _get_seed_documents_or_raise()
    normalized_bundles: list[NormalizedInstrumentBundle] = [
        normalize_source_document(document) for document in seed_documents
    ]
    if not normalized_bundles:
        raise AppServiceError(
            "No federal source documents could be normalized safely for bootstrap.",
            status_code=503,
            error_code="ingestion_normalization_unavailable",
        )
    persisted = 0
    runs = plan_federal_bootstrap_runs()

    for run in runs:
        if record_ingestion_run(run):
            persisted += 1

    bundle_persisted = 0
    for bundle in normalized_bundles:
        if upsert_instrument_bundle(bundle):
            bundle_persisted += 1

    status = "ok"
    detail = (
        "Seed metadata for federal official-source ingestion was normalized and persisted where database support is available. "
        "No retrieval publication or full corpus import was attempted."
    )
    if persisted == 0 or bundle_persisted == 0:
        status = "warning"
        detail = (
            "Federal seed metadata was normalized, but persistence is only partial or unavailable in the current environment. "
            "Admin review can still inspect the ingestion foundation, but no public retrieval publication was attempted."
        )

    return {
        "status": status,
        "planned_run_count": len(runs),
        "recorded_run_count": persisted,
        "normalized_bundle_count": len(normalized_bundles),
        "persisted_bundle_count": bundle_persisted,
        "detail": detail,
    }


def _remap_bundle_to_existing_instrument(
    bundle: NormalizedInstrumentBundle,
    matched_instrument: LegalInstrumentRecord,
) -> NormalizedInstrumentBundle:
    remapped = deepcopy(bundle)
    remapped.instrument.instrument_id = matched_instrument.instrument_id
    remapped.version.instrument_id = matched_instrument.instrument_id
    remapped.instrument.current_version_id = remapped.version.version_id

    for section in remapped.structured_sections:
        section.instrument_id = matched_instrument.instrument_id

    return remapped


def _build_duplicate_candidates(bundle: NormalizedInstrumentBundle) -> list[IngestionDuplicateCandidate]:
    duplicate_candidates: list[IngestionDuplicateCandidate] = []
    instrument_matches = find_matching_instrument_candidates(
        title=bundle.instrument.title,
        official_citation=bundle.instrument.official_citation,
        jurisdiction=bundle.instrument.jurisdiction,
        government_level=bundle.instrument.government_level,
        province=bundle.instrument.province,
    )
    version_matches = find_matching_version_candidates(
        source_url=bundle.version.source_url,
        content_hash=bundle.version.content_hash,
        instrument_id=bundle.instrument.instrument_id if instrument_exists(bundle.instrument.instrument_id) else None,
    )

    for match in instrument_matches:
        reason = "Matched by official citation." if (
            bundle.instrument.official_citation
            and match.official_citation == bundle.instrument.official_citation
        ) else "Matched by canonical title."
        duplicate_candidates.append(
            IngestionDuplicateCandidate(
                duplicate_type="instrument",
                instrument_id=match.instrument_id,
                title=match.title,
                official_citation=match.official_citation,
                source_url=match.source_url,
                reason=reason,
            )
        )

    for match in version_matches:
        if bundle.version.source_url and match.source_url == bundle.version.source_url:
            reason = "Matched by source URL."
        elif bundle.version.content_hash and match.content_hash == bundle.version.content_hash:
            reason = "Matched by content hash."
        else:
            reason = "Matched by existing instrument/version lineage."
        duplicate_candidates.append(
            IngestionDuplicateCandidate(
                duplicate_type="version",
                instrument_id=match.instrument_id,
                version_id=match.version_id,
                title=bundle.instrument.title,
                official_citation=bundle.instrument.official_citation,
                source_url=match.source_url,
                reason=reason,
            )
        )

    return duplicate_candidates


def _select_existing_instrument_candidate(
    bundle: NormalizedInstrumentBundle,
    candidates: list[IngestionDuplicateCandidate],
) -> str | None:
    for candidate in candidates:
        if candidate.duplicate_type != "instrument" or not candidate.instrument_id:
            continue
        if candidate.official_citation and candidate.official_citation == bundle.instrument.official_citation:
            return candidate.instrument_id

    for candidate in candidates:
        if candidate.duplicate_type == "instrument" and candidate.instrument_id:
            return candidate.instrument_id
    return None


def import_federal_seed_foundation() -> FederalImportPipelineResponse:
    run_label = f"federal_seed_import_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    discovery_results = run_seed_discovery(government_level="federal")
    normalization_results = run_seed_normalization(government_level="federal")
    if not discovery_results:
        raise AppServiceError(
            "No federal official-source adapters are available for import right now.",
            status_code=503,
            error_code="ingestion_adapter_unavailable",
        )
    normalized_by_adapter = {result.adapter_key: result for result in normalization_results}
    source_definitions = {source.source_slug: source for source in get_ingestion_source_registry()}

    items: list[IngestionImportItemResult] = []
    recorded_runs = 0
    imported_bundle_count = 0
    duplicate_bundle_count = 0
    discovered_document_count = sum(len(result.discovered_documents) for result in discovery_results)
    normalized_bundle_count = sum(len(result.bundles) for result in normalization_results)
    if discovered_document_count == 0 or normalized_bundle_count == 0:
        raise AppServiceError(
            "The federal ingestion foundation could not discover or normalize any official-source documents safely.",
            status_code=503,
            error_code="ingestion_discovery_empty",
        )

    for discovery in discovery_results:
        normalization = normalized_by_adapter.get(discovery.adapter_key)
        if normalization is None:
            continue

        adapter_imported = 0
        adapter_duplicates = 0
        adapter_items: list[IngestionImportItemResult] = []

        for bundle in normalization.bundles:
            duplicate_candidates = _build_duplicate_candidates(bundle)
            selected_instrument_id = _select_existing_instrument_candidate(bundle, duplicate_candidates)

            if any(candidate.duplicate_type == "version" for candidate in duplicate_candidates):
                adapter_duplicates += 1
                duplicate_bundle_count += 1
                adapter_items.append(
                    IngestionImportItemResult(
                        adapter_key=discovery.adapter_key,
                        source_slug=bundle.version.source_slug,
                        instrument_id=bundle.instrument.instrument_id,
                        version_id=bundle.version.version_id,
                        title=bundle.instrument.title,
                        official_citation=bundle.instrument.official_citation,
                        source_url=bundle.version.source_url,
                        outcome="duplicate_skipped",
                        provenance_summary=(
                            f"{bundle.version.source_authority or bundle.version.source_slug} "
                            f"({bundle.version.source_trust_level})"
                        ),
                        duplicate_candidates=duplicate_candidates,
                    )
                )
                continue

            effective_bundle = bundle
            if selected_instrument_id:
                effective_bundle = _remap_bundle_to_existing_instrument(
                    bundle,
                    LegalInstrumentRecord(
                        instrument_id=selected_instrument_id,
                        title=bundle.instrument.title,
                        category=bundle.instrument.category,
                        law_type=bundle.instrument.law_type,
                    ),
                )

            if upsert_instrument_bundle(effective_bundle):
                adapter_imported += 1
                imported_bundle_count += 1
                outcome = "imported_attached_to_existing_instrument" if selected_instrument_id else "imported_new_instrument"
            else:
                outcome = "persistence_unavailable"

            adapter_items.append(
                IngestionImportItemResult(
                    adapter_key=discovery.adapter_key,
                    source_slug=effective_bundle.version.source_slug,
                    instrument_id=effective_bundle.instrument.instrument_id,
                    version_id=effective_bundle.version.version_id,
                    title=effective_bundle.instrument.title,
                    official_citation=effective_bundle.instrument.official_citation,
                    source_url=effective_bundle.version.source_url,
                    outcome=outcome,
                    provenance_summary=(
                        f"{effective_bundle.version.source_authority or effective_bundle.version.source_slug} "
                        f"({effective_bundle.version.source_trust_level})"
                    ),
                    duplicate_candidates=duplicate_candidates,
                )
            )

        items.extend(adapter_items)

        run = IngestionRunRecord(
            run_id=f"{run_label}-{discovery.adapter_key}-{uuid4().hex[:8]}",
            adapter_key=discovery.adapter_key,
            scope_label=run_label,
            jurisdiction="Pakistan",
            government_level=source_definitions.get(discovery.adapter_key, IngestionSourceDefinition(
                source_slug=discovery.adapter_key,
                label=discovery.adapter_key,
                trust_level="unknown",
                source_homepage="",
                update_mode="seed_import",
                coverage_scope="federal bootstrap",
                source_notes="",
                source_authority=discovery.adapter_key,
            )).government_level,
            status="completed",
            discovered_documents=len(discovery.discovered_documents),
            imported_instruments=sum(1 for item in adapter_items if item.outcome == "imported_new_instrument"),
            imported_versions=sum(
                1
                for item in adapter_items
                if item.outcome in {"imported_new_instrument", "imported_attached_to_existing_instrument"}
            ),
            imported_provisions=0,
            duplicate_candidates=adapter_duplicates,
            run_metadata={
                "run_label": run_label,
                "notes": [*discovery.notes, *normalization.notes],
                "workflow_stage": "federal_seed_foundation",
                "source_authority": source_definitions.get(discovery.adapter_key).source_authority
                if source_definitions.get(discovery.adapter_key)
                else discovery.adapter_key,
                "source_priority": source_definitions.get(discovery.adapter_key).source_priority
                if source_definitions.get(discovery.adapter_key)
                else None,
                "item_outcomes": [item.outcome for item in adapter_items],
            },
            started_at=datetime.now(timezone.utc).isoformat(),
            finished_at=datetime.now(timezone.utc).isoformat(),
        )
        if record_ingestion_run(run):
            recorded_runs += 1

    response_status = "ok"
    workflow_note = (
        "This first-pass federal import only ingests a small official-source seed set, preserves source provenance, "
        "skips exact version duplicates, and leaves all imported records in an admin-review state."
    )
    if imported_bundle_count == 0 and duplicate_bundle_count == 0:
        response_status = "warning"
        workflow_note = (
            "The federal import run completed safely but did not persist any new bundles. "
            "Check source availability, persistence readiness, and admin review prerequisites before retrying. "
            "No public legal-information publication was attempted."
        )
    elif recorded_runs == 0:
        response_status = "warning"
        workflow_note = (
            "Federal source bundles were evaluated, but ingestion-run persistence is unavailable in the current environment. "
            "Source provenance remains part of the response, and no public retrieval publication was attempted."
        )

    return FederalImportPipelineResponse(
        status=response_status,
        run_label=run_label,
        discovered_document_count=discovered_document_count,
        normalized_bundle_count=normalized_bundle_count,
        imported_bundle_count=imported_bundle_count,
        duplicate_bundle_count=duplicate_bundle_count,
        runs_recorded=recorded_runs,
        items=items,
        workflow_note=workflow_note,
    )
