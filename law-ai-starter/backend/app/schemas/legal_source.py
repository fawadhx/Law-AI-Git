from pydantic import BaseModel, Field


class LegalSourceRecord(BaseModel):
    id: str
    source_title: str
    law_name: str
    section_number: str
    section_title: str
    summary: str
    excerpt: str
    citation_label: str
    jurisdiction: str = "Pakistan"
    tags: list[str] = Field(default_factory=list)