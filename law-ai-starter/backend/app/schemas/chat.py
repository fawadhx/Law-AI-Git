from pydantic import BaseModel, Field


class Citation(BaseModel):
    title: str
    section: str
    note: str
    excerpt: str = ""


class ChatCategory(BaseModel):
    key: str
    label: str


class ChatConfidence(BaseModel):
    level: str
    score: int
    matched_records: int


class ChatQueryRequest(BaseModel):
    question: str


class ChatQueryResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    disclaimer: str
    category: ChatCategory
    confidence: ChatConfidence