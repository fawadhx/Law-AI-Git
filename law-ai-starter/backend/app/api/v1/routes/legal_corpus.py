from fastapi import APIRouter, Depends

from app.api.deps.admin_auth import require_admin_auth, require_admin_write_access
from app.schemas.legal_corpus import (
    FederalImportPipelineResponse,
    LegalCorpusBootstrapResponse,
    LegalCorpusFoundationResponse,
    LegalCorpusInstrumentCatalogResponse,
    LegalCorpusSyncPlanResponse,
)
from app.services.legal_import_service import bootstrap_federal_seed_metadata, import_federal_seed_foundation
from app.services.legal_corpus_service import (
    get_legal_corpus_foundation,
    get_legal_corpus_instrument_catalog,
    get_legal_corpus_sync_plan,
)
from app.services.admin_audit_service import write_admin_audit_event

router = APIRouter(dependencies=[Depends(require_admin_auth)])


@router.get("/admin/legal-corpus/foundation", response_model=LegalCorpusFoundationResponse)
def admin_legal_corpus_foundation() -> LegalCorpusFoundationResponse:
    return get_legal_corpus_foundation()


@router.get("/admin/legal-corpus/instruments", response_model=LegalCorpusInstrumentCatalogResponse)
def admin_legal_corpus_instruments() -> LegalCorpusInstrumentCatalogResponse:
    return get_legal_corpus_instrument_catalog()


@router.get("/admin/legal-corpus/sync-plan", response_model=LegalCorpusSyncPlanResponse)
def admin_legal_corpus_sync_plan() -> LegalCorpusSyncPlanResponse:
    return get_legal_corpus_sync_plan()


@router.post("/admin/legal-corpus/bootstrap-federal-seeds", response_model=LegalCorpusBootstrapResponse)
def admin_bootstrap_federal_seed_metadata(
    _: object = Depends(require_admin_write_access),
) -> LegalCorpusBootstrapResponse:
    result = bootstrap_federal_seed_metadata()
    response = LegalCorpusBootstrapResponse(
        status=str(result.get("status", "ok") or "ok"),
        planned_run_count=int(result.get("planned_run_count", 0) or 0),
        recorded_run_count=int(result.get("recorded_run_count", 0) or 0),
        normalized_bundle_count=int(result.get("normalized_bundle_count", 0) or 0),
        persisted_bundle_count=int(result.get("persisted_bundle_count", 0) or 0),
        detail=str(result.get("detail", "")),
    )
    write_admin_audit_event(
        kind="legal_corpus_bootstrap",
        title="Bootstrapped federal seed metadata",
        detail=response.detail,
        status=response.status,
        metadata={
            "planned_run_count": response.planned_run_count,
            "recorded_run_count": response.recorded_run_count,
            "normalized_bundle_count": response.normalized_bundle_count,
            "persisted_bundle_count": response.persisted_bundle_count,
        },
    )
    return response


@router.post("/admin/legal-corpus/import-federal-foundation", response_model=FederalImportPipelineResponse)
def admin_import_federal_foundation(
    _: object = Depends(require_admin_write_access),
) -> FederalImportPipelineResponse:
    response = import_federal_seed_foundation()
    write_admin_audit_event(
        kind="legal_corpus_import",
        title="Imported federal foundation seed set",
        detail=response.workflow_note,
        status=response.status,
        metadata={
            "run_label": response.run_label,
            "discovered_document_count": response.discovered_document_count,
            "normalized_bundle_count": response.normalized_bundle_count,
            "imported_bundle_count": response.imported_bundle_count,
            "duplicate_bundle_count": response.duplicate_bundle_count,
            "runs_recorded": response.runs_recorded,
        },
    )
    return response
