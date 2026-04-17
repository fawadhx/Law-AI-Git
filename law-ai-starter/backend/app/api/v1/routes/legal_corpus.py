from fastapi import APIRouter, Depends

from app.api.deps.admin_auth import require_admin_auth, require_admin_write_access
from app.schemas.legal_corpus import (
    LegalCorpusBootstrapResponse,
    LegalCorpusFoundationResponse,
    LegalCorpusInstrumentCatalogResponse,
)
from app.services.legal_import_service import bootstrap_federal_seed_metadata
from app.services.legal_corpus_service import (
    get_legal_corpus_foundation,
    get_legal_corpus_instrument_catalog,
)

router = APIRouter(dependencies=[Depends(require_admin_auth)])


@router.get("/admin/legal-corpus/foundation", response_model=LegalCorpusFoundationResponse)
def admin_legal_corpus_foundation() -> LegalCorpusFoundationResponse:
    return get_legal_corpus_foundation()


@router.get("/admin/legal-corpus/instruments", response_model=LegalCorpusInstrumentCatalogResponse)
def admin_legal_corpus_instruments() -> LegalCorpusInstrumentCatalogResponse:
    return get_legal_corpus_instrument_catalog()


@router.post("/admin/legal-corpus/bootstrap-federal-seeds", response_model=LegalCorpusBootstrapResponse)
def admin_bootstrap_federal_seed_metadata(
    _: object = Depends(require_admin_write_access),
) -> LegalCorpusBootstrapResponse:
    result = bootstrap_federal_seed_metadata()
    return LegalCorpusBootstrapResponse(
        status="ok",
        planned_run_count=int(result.get("planned_run_count", 0) or 0),
        recorded_run_count=int(result.get("recorded_run_count", 0) or 0),
        normalized_bundle_count=int(result.get("normalized_bundle_count", 0) or 0),
        persisted_bundle_count=int(result.get("persisted_bundle_count", 0) or 0),
        detail=(
            "Seed metadata for federal official-source ingestion was normalized and persisted where database support is available. "
            "No retrieval publication or full corpus import was attempted."
        ),
    )
