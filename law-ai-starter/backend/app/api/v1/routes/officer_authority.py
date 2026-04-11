from fastapi import APIRouter

from app.schemas.officer_authority import OfficerAuthorityResponse
from app.services.officer_authority_service import get_officer_authority

router = APIRouter()


@router.get("/officer-authority/{rank}", response_model=OfficerAuthorityResponse)
def officer_authority_lookup(rank: str) -> OfficerAuthorityResponse:
    return get_officer_authority(rank)