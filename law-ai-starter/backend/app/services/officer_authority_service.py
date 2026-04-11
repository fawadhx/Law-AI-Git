from fastapi import HTTPException

from app.data.officer_authority import OFFICER_AUTHORITY_DATA
from app.schemas.officer_authority import OfficerAuthorityResponse


def get_officer_authority(rank: str) -> OfficerAuthorityResponse:
    normalized_rank = rank.strip().lower()
    record = OFFICER_AUTHORITY_DATA.get(normalized_rank)

    if not record:
        raise HTTPException(status_code=404, detail="Officer rank not found.")

    return OfficerAuthorityResponse(**record)