from pydantic import BaseModel, Field


class Citation(BaseModel):
    title: str
    section: str
    note: str


class ChatQueryRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=2000)


class ChatQueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    disclaimer: str