from fastapi import APIRouter, HTTPException

from app.schemas.officer import OfficerAuthorityResponse
from app.services.officer_service import lookup_officer_authority

router = APIRouter()


@router.get("/{rank}", response_model=OfficerAuthorityResponse)
def get_officer_authority(rank: str) -> OfficerAuthorityResponse:
    result = lookup_officer_authority(rank)
    if result is None:
        raise HTTPException(status_code=404, detail="Officer rank not found.")
    return result
