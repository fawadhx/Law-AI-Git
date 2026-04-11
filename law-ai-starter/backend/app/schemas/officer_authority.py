from pydantic import BaseModel


class OfficerAuthorityResponse(BaseModel):
    rank: str
    summary: str
    powers: list[str]
    limitations: list[str]