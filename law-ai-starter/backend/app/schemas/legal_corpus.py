from __future__ import annotations

from pydantic import BaseModel, Field


GovernmentLevel = str
LawType = str
PublicationStatus = str
ReviewStatus = str
SourceTrustLevel = str
IngestionRunStatus = str


class LegalInstrumentRecord(BaseModel):
    instrument_id: str
    title: str
    short_title: str | None = None
    jurisdiction: str = "Pakistan"
    government_level: GovernmentLevel = "federal"
    province: str | None = None
    category: str
    law_type: LawType
    promulgation_date: str | None = None
    effective_date: str | None = None
    status: PublicationStatus = "unknown"
    official_citation: str | None = None
    source_url: str | None = None
    gazette_reference: str | None = None
    language: str = "en"
    current_version_id: str | None = None
    amendment_notes: str | None = None
    admin_review_status: ReviewStatus = "imported_unreviewed"
    provenance_source_slug: str | None = None


class LegalInstrumentVersionRecord(BaseModel):
    version_id: str
    instrument_id: str
    source_slug: str
    source_url: str
    source_trust_level: SourceTrustLevel
    version_label: str | None = None
    version_date: str | None = None
    promulgation_date: str | None = None
    effective_date: str | None = None
    publication_status: PublicationStatus = "unknown"
    language: str = "en"
    content_hash: str | None = None
    source_format: str = "html"
    gazette_reference: str | None = None
    amendment_notes: str | None = None
    raw_text: str | None = None
    cleaned_text: str | None = None
    admin_review_status: ReviewStatus = "imported_unreviewed"
    extraction_metadata: dict[str, object] = Field(default_factory=dict)


class LegalProvisionRecord(BaseModel):
    provision_id: str
    instrument_id: str
    version_id: str
    provision_path: str
    part_number: str | None = None
    chapter_number: str | None = None
    section_number: str | None = None
    subsection_number: str | None = None
    heading: str | None = None
    body_text: str
    summary: str | None = None
    citations: list[str] = Field(default_factory=list)
    sort_index: int = 0
    retrieval_ready: bool = False


class IngestionSourceDefinition(BaseModel):
    source_slug: str
    label: str
    jurisdiction: str = "Pakistan"
    government_level: GovernmentLevel = "federal"
    trust_level: SourceTrustLevel
    source_homepage: str
    update_mode: str
    coverage_scope: str
    supported_law_types: list[str] = Field(default_factory=list)
    supported_languages: list[str] = Field(default_factory=list)
    source_notes: str
    ingestion_stage: str = "planned"
    active: bool = True


class RawSourceDocumentInput(BaseModel):
    source_slug: str
    source_url: str
    title: str
    short_title: str | None = None
    jurisdiction: str = "Pakistan"
    government_level: GovernmentLevel = "federal"
    province: str | None = None
    category: str
    law_type: LawType
    promulgation_date: str | None = None
    effective_date: str | None = None
    status: PublicationStatus = "unknown"
    official_citation: str | None = None
    gazette_reference: str | None = None
    language: str = "en"
    version_label: str | None = None
    version_date: str | None = None
    amendment_notes: str | None = None
    source_format: str = "html"
    source_trust_level: SourceTrustLevel
    raw_text: str | None = None
    cleaned_text: str | None = None
    extraction_metadata: dict[str, object] = Field(default_factory=dict)


class IngestionRunRecord(BaseModel):
    run_id: str
    adapter_key: str
    scope_label: str
    jurisdiction: str
    government_level: GovernmentLevel
    status: IngestionRunStatus
    discovered_documents: int = 0
    imported_instruments: int = 0
    imported_versions: int = 0
    imported_provisions: int = 0
    duplicate_candidates: int = 0
    run_metadata: dict[str, object] = Field(default_factory=dict)
    started_at: str | None = None
    finished_at: str | None = None


class LegalCorpusLayerInfo(BaseModel):
    layer: str
    storage_target: str
    purpose: str


class ReviewFieldDescriptor(BaseModel):
    key: str
    label: str
    description: str
    required: bool = True


class LegalCorpusSourcePreview(BaseModel):
    source_slug: str
    source_label: str
    trust_level: SourceTrustLevel
    sample_document_title: str
    source_url: str
    official_citation: str | None = None
    gazette_reference: str | None = None
    law_type: LawType
    category: str
    government_level: GovernmentLevel
    promulgation_date: str | None = None
    effective_date: str | None = None
    status: PublicationStatus
    language: str
    admin_review_status: ReviewStatus = "imported_unreviewed"
    provenance_summary: str
    extraction_notes: list[str] = Field(default_factory=list)


class LegalCorpusStorageSnapshot(BaseModel):
    persistence_mode: str
    database_ready: bool
    instruments: int = 0
    versions: int = 0
    provisions: int = 0
    ingestion_runs: int = 0
    tables: list[str] = Field(default_factory=list)


class NormalizedInstrumentBundle(BaseModel):
    instrument: LegalInstrumentRecord
    version: LegalInstrumentVersionRecord
    provisions: list[LegalProvisionRecord] = Field(default_factory=list)


class LegalCorpusFoundationResponse(BaseModel):
    generated_at: str
    storage: LegalCorpusStorageSnapshot
    canonical_layers: list[LegalCorpusLayerInfo] = Field(default_factory=list)
    source_registry: list[IngestionSourceDefinition] = Field(default_factory=list)
    review_fields: list[ReviewFieldDescriptor] = Field(default_factory=list)
    source_previews: list[LegalCorpusSourcePreview] = Field(default_factory=list)
    planned_runs: list[IngestionRunRecord] = Field(default_factory=list)
    implementation_notes: list[str] = Field(default_factory=list)


class LegalCorpusBootstrapResponse(BaseModel):
    status: str
    planned_run_count: int
    recorded_run_count: int
    normalized_bundle_count: int
    persisted_bundle_count: int
    detail: str


class LegalCorpusInstrumentCatalogResponse(BaseModel):
    total_records: int
    items: list[LegalInstrumentRecord] = Field(default_factory=list)
    workflow_note: str
