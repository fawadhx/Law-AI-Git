from fastapi import APIRouter

from app.schemas.admin import AdminSourceCatalogResponse, AdminSummaryResponse
from app.services.admin_service import get_admin_source_catalog, get_admin_summary

router = APIRouter()


@router.get("/admin/summary", response_model=AdminSummaryResponse)
def admin_summary() -> AdminSummaryResponse:
    return get_admin_summary()


@router.get("/admin/sources", response_model=AdminSourceCatalogResponse)
def admin_sources() -> AdminSourceCatalogResponse:
    return get_admin_source_catalog()
