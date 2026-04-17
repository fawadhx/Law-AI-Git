from pydantic import BaseModel, Field


class Citation(BaseModel):
    title: str
    section: str
    note: str
    excerpt: str = ""
    provenance: str | None = None
    source_url: str | None = None


class ChatCategory(BaseModel):
    key: str
    label: str


class ChatConfidence(BaseModel):
    level: str
    score: int
    matched_records: int


class MatchExplanation(BaseModel):
    title: str
    points: list[str] = Field(default_factory=list)


class ChatQueryRequest(BaseModel):
    question: str


class ChatQueryResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    disclaimer: str
    category: ChatCategory
    confidence: ChatConfidence
    why_matched: list[MatchExplanation] = Field(default_factory=list)
