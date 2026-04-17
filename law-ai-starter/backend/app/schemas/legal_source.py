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
    aliases: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    related_sections: list[str] = Field(default_factory=list)
    offence_group: str | None = None
    punishment_summary: str | None = None
    provision_kind: str = "general"
    retrieval_document: str | None = None
    retrieval_fingerprint: str | None = None
    embedding_status: str | None = None
    embedding_model: str | None = None
    embedding_dimensions: int | None = None
    embedding_updated_at: str | None = None
    source_url: str | None = None
    provenance: str | None = None
    source_trust_level: str | None = None
    retrieval_source_type: str = "prototype"

    @property
    def searchable_parts(self) -> list[str]:
        return [
            self.source_title,
            self.law_name,
            self.section_number,
            self.section_title,
            self.summary,
            self.excerpt,
            self.citation_label,
            " ".join(self.tags),
            " ".join(self.aliases),
            " ".join(self.keywords),
            " ".join(self.related_sections),
            self.offence_group or "",
            self.punishment_summary or "",
            self.provision_kind,
            self.provenance or "",
            self.source_url or "",
            self.source_trust_level or "",
            self.retrieval_source_type,
        ]
