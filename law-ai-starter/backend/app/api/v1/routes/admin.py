from fastapi import APIRouter, HTTPException

from app.schemas.admin import (
    AdminSourceCatalogResponse,
    AdminSourceDetailResponse,
    AdminSummaryResponse,
)
from app.services.admin_service import (
    get_admin_source_catalog,
    get_admin_source_detail,
    get_admin_summary,
)

router = APIRouter()


@router.get("/admin/summary", response_model=AdminSummaryResponse)
def admin_summary() -> AdminSummaryResponse:
    return get_admin_summary()


@router.get("/admin/sources", response_model=AdminSourceCatalogResponse)
def admin_sources() -> AdminSourceCatalogResponse:
    return get_admin_source_catalog()


@router.get("/admin/sources/{source_id}", response_model=AdminSourceDetailResponse)
def admin_source_detail(source_id: str) -> AdminSourceDetailResponse:
    detail = get_admin_source_detail(source_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Source record not found.")
    return detail
