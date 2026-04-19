from pydantic import BaseModel, Field


class AdminStat(BaseModel):
    value: str
    title: str
    description: str


class AdminStatusCard(BaseModel):
    title: str
    content: str


class AdminRoadmapItem(BaseModel):
    title: str
    text: str




class AdminCatalogSourceInfo(BaseModel):
    active_source: str
    source_label: str
    database_ready: bool
    foundation_stage: str
    active_record_count: int
    persisted_record_count: int
    detail: str


class AdminSummaryResponse(BaseModel):
    stats: list[AdminStat]
    control_areas: list[AdminRoadmapItem]
    status_cards: list[AdminStatusCard]
    workflow_steps: list[str]
    roadmap_items: list[AdminRoadmapItem]
    admin_boundary: str
    catalog_source: AdminCatalogSourceInfo | None = None


class AdminSourceRecord(BaseModel):
    id: str
    citation_label: str
    source_title: str
    law_name: str
    section_number: str
    section_title: str
    summary: str
    country: str = "Pakistan"
    jurisdiction: str
    jurisdiction_type: str = "federal"
    government_level: str = "federal"
    province: str | None = None
    law_category: str | None = None
    law_type: str | None = None
    official_citation: str | None = None
    source_status: str | None = None
    provision_kind: str
    offence_group: str | None = None
    related_sections: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    punishment_summary: str | None = None
    admin_note: str


class AdminSourceCatalogSummary(BaseModel):
    total_records: int
    law_count: int
    offence_group_count: int
    punishment_record_count: int
    procedure_record_count: int


class AdminSourceCatalogResponse(BaseModel):
    summary: AdminSourceCatalogSummary
    catalog_source: AdminCatalogSourceInfo | None = None
    items: list[AdminSourceRecord]
    available_laws: list[str]
    available_provinces: list[str] = Field(default_factory=list)
    available_groups: list[str]
    available_kinds: list[str]
    workflow_note: str


class AdminLinkedRecord(BaseModel):
    id: str
    citation_label: str
    law_name: str
    section_number: str
    section_title: str
    provision_kind: str
    relationship_label: str
    summary: str


class AdminSourceDetailRecord(AdminSourceRecord):
    excerpt: str
    aliases: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    searchable_terms: list[str] = Field(default_factory=list)
    enactment_year: int | None = None
    effective_year: int | None = None
    source_url: str | None = None
    source_last_verified: str | None = None
    source_trust_level: str | None = None
    amendment_notes: str | None = None
    provenance: str | None = None
    related_record_count: int = 0
    same_group_record_count: int = 0
    same_law_record_count: int = 0


class AdminSourceDetailResponse(BaseModel):
    item: AdminSourceDetailRecord
    catalog_source: AdminCatalogSourceInfo | None = None
    companion_records: list[AdminLinkedRecord] = Field(default_factory=list)
    same_group_records: list[AdminLinkedRecord] = Field(default_factory=list)
    same_law_records: list[AdminLinkedRecord] = Field(default_factory=list)
    version_count: int = 0
    latest_version_number: int | None = None
    workflow_note: str


class AdminSourceDraftInput(BaseModel):
    id: str | None = None
    source_title: str = ""
    law_name: str = ""
    section_number: str = ""
    section_title: str = ""
    summary: str = ""
    excerpt: str = ""
    citation_label: str = ""
    country: str = "Pakistan"
    jurisdiction: str = "Pakistan"
    jurisdiction_type: str = "federal"
    government_level: str = "federal"
    province: str = ""
    law_category: str = ""
    law_type: str = ""
    source_status: str = ""
    official_citation: str = ""
    enactment_year: int | None = None
    effective_year: int | None = None
    tags: list[str] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    related_sections: list[str] = Field(default_factory=list)
    offence_group: str | None = None
    punishment_summary: str | None = None
    provision_kind: str = "general"
    source_url: str = ""
    source_last_verified: str = ""
    amendment_notes: str = ""
    source_trust_level: str = ""


class AdminDraftValidationIssue(BaseModel):
    field: str
    level: str
    message: str


class AdminDraftSectionCheck(BaseModel):
    existing: list[str] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)


class AdminSourceDraftPreview(BaseModel):
    citation_label: str
    law_name: str
    section_number: str
    section_title: str
    provision_kind: str
    offence_group: str | None = None
    related_sections: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    searchable_terms: list[str] = Field(default_factory=list)
    admin_note: str


class AdminSourceDraftValidationResponse(BaseModel):
    preview: AdminSourceDraftPreview
    readiness_score: int
    issue_count: int
    error_count: int
    warning_count: int
    issues: list[AdminDraftValidationIssue] = Field(default_factory=list)
    related_section_check: AdminDraftSectionCheck
    workflow_note: str


class AdminDraftFieldChange(BaseModel):
    field: str
    label: str
    before: str | None = None
    after: str | None = None
    changed: bool


class AdminReviewChecklistItem(BaseModel):
    key: str
    title: str
    status: str
    detail: str


class AdminSourceDraftReviewResponse(BaseModel):
    review_status: str
    approval_label: str
    readiness_score: int
    blocker_count: int
    warning_count: int
    publish_mode: str
    changed_field_count: int
    changed_fields: list[AdminDraftFieldChange] = Field(default_factory=list)
    checklist: list[AdminReviewChecklistItem] = Field(default_factory=list)
    workflow_note: str


class AdminSourcePublishPreviewResponse(BaseModel):
    publish_status: str
    publish_mode: str
    target_record_id: str | None = None
    changed_field_count: int
    searchable_term_count: int
    linked_section_count: int
    companion_hit_count: int
    same_group_context_count: int
    same_law_context_count: int
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    changed_fields: list[AdminDraftFieldChange] = Field(default_factory=list)
    workflow_note: str


class AdminWorkspaceDraftSaveRequest(BaseModel):
    workspace_draft_id: str | None = None
    label: str | None = None
    draft: AdminSourceDraftInput


class AdminWorkspaceStageRequest(BaseModel):
    workspace_draft_id: str | None = None
    draft: AdminSourceDraftInput


class AdminWorkspaceDraftRecord(BaseModel):
    workspace_draft_id: str
    title: str
    citation_label: str
    law_name: str
    section_number: str
    publish_mode: str
    source_record_id: str | None = None
    version: int = 1
    readiness_score: int
    review_status: str
    publish_status: str
    blocker_count: int
    warning_count: int
    changed_field_count: int
    saved_at: str


class AdminWorkspaceDraftDetailResponse(BaseModel):
    workspace_draft: AdminWorkspaceDraftRecord
    payload: AdminSourceDraftInput
    validation: AdminSourceDraftValidationResponse
    review: AdminSourceDraftReviewResponse
    publish_preview: AdminSourcePublishPreviewResponse
    workflow_note: str


class AdminPublishQueueRecord(BaseModel):
    package_id: str
    workspace_draft_id: str | None = None
    title: str
    citation_label: str
    publish_mode: str
    target_record_id: str | None = None
    review_status: str
    publish_status: str
    blocker_count: int
    warning_count: int
    changed_field_count: int
    staged_at: str
    summary_line: str


class AdminWorkspaceResponse(BaseModel):
    saved_draft_count: int
    staged_publish_count: int
    ready_draft_count: int
    blocked_item_count: int
    session_publish_count: int = 0
    drafts: list[AdminWorkspaceDraftRecord] = Field(default_factory=list)
    publish_queue: list[AdminPublishQueueRecord] = Field(default_factory=list)
    workflow_note: str


class AdminActivityRecord(BaseModel):
    activity_id: str
    kind: str
    title: str
    detail: str
    status: str
    citation_label: str | None = None
    record_id: str | None = None
    created_at: str


class AdminActivityFeedResponse(BaseModel):
    total_events: int
    publish_event_count: int
    latest_publish_label: str | None = None
    items: list[AdminActivityRecord] = Field(default_factory=list)
    workflow_note: str


class AdminSourceVersionRecord(BaseModel):
    version_id: str
    record_id: str
    version_number: int
    action: str
    citation_label: str
    title: str
    changed_fields: list[AdminDraftFieldChange] = Field(default_factory=list)
    changed_field_count: int = 0
    actor_username: str | None = None
    actor_role: str | None = None
    audit_id: str | None = None
    created_at: str


class AdminSourceHistoryResponse(BaseModel):
    record_id: str | None = None
    total_versions: int
    latest_version_number: int | None = None
    items: list[AdminSourceVersionRecord] = Field(default_factory=list)
    workflow_note: str


class AdminPublishExecutionResponse(BaseModel):
    publish_status: str
    package_id: str
    published_record_id: str
    citation_label: str
    publish_mode: str
    changed_field_count: int
    catalog_record_count: int
    activity: AdminActivityRecord
    workflow_note: str


class AdminRetrievalReadinessRecord(BaseModel):
    record_id: str
    citation_label: str
    law_name: str
    section_number: str
    embedding_status: str
    has_retrieval_document: bool
    has_retrieval_fingerprint: bool
    fingerprint_status: str
    refresh_needed: bool


class AdminRetrievalReadinessResponse(BaseModel):
    active_source: str
    source_label: str
    database_ready: bool
    foundation_stage: str
    persisted_record_count: int
    active_record_count: int
    embedding_ready_count: int
    embedding_pending_count: int
    stale_count: int
    missing_document_count: int
    missing_fingerprint_count: int
    refresh_needed_count: int
    vector_candidate_count: int
    sample_records: list[AdminRetrievalReadinessRecord] = Field(default_factory=list)
    workflow_note: str


class AdminRetrievalRefreshRequest(BaseModel):
    force_all: bool = False


class AdminRetrievalRefreshResponse(BaseModel):
    refresh_applied: bool
    active_source: str
    source_label: str
    refreshed_count: int
    unchanged_count: int
    pending_marked_count: int
    persisted_record_count: int
    embedding_ready_count: int
    embedding_pending_count: int
    sample_records: list[AdminRetrievalReadinessRecord] = Field(default_factory=list)
    workflow_note: str


class AdminEmbeddingReadinessRecord(BaseModel):
    record_id: str
    citation_label: str
    law_name: str
    section_number: str
    embedding_status: str
    has_vector: bool
    fingerprint_match: bool
    model_name: str | None = None
    dimensions: int | None = None
    refresh_needed: bool
    last_error: str | None = None


class AdminEmbeddingReadinessResponse(BaseModel):
    provider_ready: bool
    api_key_configured: bool
    active_source: str
    source_label: str
    database_ready: bool
    foundation_stage: str
    persisted_record_count: int
    vector_row_count: int
    ready_vector_count: int
    pending_count: int
    error_count: int
    runnable_count: int
    sample_records: list[AdminEmbeddingReadinessRecord] = Field(default_factory=list)
    workflow_note: str


class AdminEmbeddingRunRequest(BaseModel):
    limit: int = 10
    record_ids: list[str] = Field(default_factory=list)


class AdminEmbeddingRunResponse(BaseModel):
    run_attempted: bool
    provider_ready: bool
    api_key_configured: bool
    active_source: str
    source_label: str
    database_ready: bool
    foundation_stage: str
    persisted_record_count: int
    vector_row_count: int
    ready_vector_count: int
    pending_count: int
    error_count: int
    runnable_count: int
    processed_count: int
    success_count: int
    skipped_count: int
    sample_records: list[AdminEmbeddingReadinessRecord] = Field(default_factory=list)
    workflow_note: str


class AdminRetrievalProbeRequest(BaseModel):
    query: str
    limit: int = 6


class AdminRetrievalProbeRecord(BaseModel):
    record_id: str
    citation_label: str
    law_name: str
    section_number: str
    category: str
    keyword_score: int
    vector_similarity: float | None = None
    vector_bonus: int
    final_score: int
    selected: bool
    exact_section_match: bool
    excerpt: str


class AdminRetrievalProbeResponse(BaseModel):
    query: str
    active_source: str
    source_label: str
    vector_retrieval_active: bool
    vector_query_top_k: int
    keyword_candidate_count: int
    vector_candidate_count: int
    selected_count: int
    records: list[AdminRetrievalProbeRecord] = Field(default_factory=list)
    workflow_note: str


class AdminSourceCreateResponse(BaseModel):
    create_status: str
    save_mode: str
    record_id: str | None = None
    citation_label: str = ""
    persisted_sync_applied: bool = False
    item: AdminSourceRecord | None = None
    validation: AdminSourceDraftValidationResponse
    workflow_note: str


class AdminSourceUpdateResponse(BaseModel):
    update_status: str
    save_mode: str
    record_id: str | None = None
    citation_label: str = ""
    retrieval_changed: bool = False
    persisted_sync_applied: bool = False
    item: AdminSourceRecord | None = None
    validation: AdminSourceDraftValidationResponse
    workflow_note: str


class AdminSourceDeleteResponse(BaseModel):
    delete_status: str
    save_mode: str
    record_id: str | None = None
    citation_label: str = ""
    persisted_sync_applied: bool = False
    deleted_title: str = ""
    workflow_note: str


class AdminIngestionPreviewRequest(BaseModel):
    raw_text: str = ""
    source_title: str = ""
    law_name: str = ""
    jurisdiction: str = "Pakistan"
    citation_hint: str = ""


class AdminIngestionDuplicateCandidate(BaseModel):
    record_id: str
    citation_label: str
    section_title: str
    law_name: str
    match_reason: str


class AdminIngestionPreviewResponse(BaseModel):
    draft: AdminSourceDraftInput
    validation: AdminSourceDraftValidationResponse
    extracted_title: str = ""
    extracted_section_number: str = ""
    extracted_section_title: str = ""
    duplicate_candidates: list[AdminIngestionDuplicateCandidate] = Field(default_factory=list)
    workflow_note: str


class AdminIngestionBatchPreviewRequest(BaseModel):
    raw_text: str = ""
    source_title: str = ""
    law_name: str = ""
    jurisdiction: str = "Pakistan"
    citation_hint: str = ""
    max_candidates: int = 5


class AdminIngestionBatchPreviewResponse(BaseModel):
    items: list[AdminIngestionPreviewResponse] = Field(default_factory=list)
    item_count: int = 0
    workflow_note: str
