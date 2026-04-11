from fastapi import APIRouter

from app.schemas.admin import AdminSummaryResponse
from app.services.admin_service import get_admin_summary

router = APIRouter()


@router.get("/admin/summary", response_model=AdminSummaryResponse)
def admin_summary() -> AdminSummaryResponse:
    return get_admin_summary()