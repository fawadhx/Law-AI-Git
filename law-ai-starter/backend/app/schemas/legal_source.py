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
    country: str = "Pakistan"
    jurisdiction: str = "Pakistan"
    jurisdiction_type: str = "federal"
    government_level: str = "federal"
    province: str | None = None
    law_category: str | None = None
    law_type: str | None = None
    source_status: str | None = None
    official_citation: str | None = None
    enactment_year: int | None = None
    effective_year: int | None = None
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
    source_last_verified: str | None = None
    amendment_notes: str | None = None
    provenance: str | None = None
    source_trust_level: str | None = None
    retrieval_source_type: str = "legacy_catalog"

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
            self.country,
            self.government_level,
            self.jurisdiction_type,
            self.province or "",
            self.law_category or "",
            self.law_type or "",
            self.source_status or "",
            self.official_citation or "",
            str(self.enactment_year or ""),
            str(self.effective_year or ""),
            " ".join(self.tags),
            " ".join(self.aliases),
            " ".join(self.keywords),
            " ".join(self.related_sections),
            self.offence_group or "",
            self.punishment_summary or "",
            self.provision_kind,
            self.amendment_notes or "",
            self.provenance or "",
            self.source_url or "",
            self.source_last_verified or "",
            self.source_trust_level or "",
            self.retrieval_source_type,
        ]
