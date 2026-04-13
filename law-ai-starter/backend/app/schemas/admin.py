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


class AdminSummaryResponse(BaseModel):
    stats: list[AdminStat]
    control_areas: list[AdminRoadmapItem]
    status_cards: list[AdminStatusCard]
    workflow_steps: list[str]
    roadmap_items: list[AdminRoadmapItem]
    admin_boundary: str


class AdminSourceRecord(BaseModel):
    id: str
    citation_label: str
    source_title: str
    law_name: str
    section_number: str
    section_title: str
    summary: str
    jurisdiction: str
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
    items: list[AdminSourceRecord]
    available_laws: list[str]
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
    related_record_count: int = 0
    same_group_record_count: int = 0
    same_law_record_count: int = 0


class AdminSourceDetailResponse(BaseModel):
    item: AdminSourceDetailRecord
    companion_records: list[AdminLinkedRecord] = Field(default_factory=list)
    same_group_records: list[AdminLinkedRecord] = Field(default_factory=list)
    same_law_records: list[AdminLinkedRecord] = Field(default_factory=list)
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
    jurisdiction: str = "Pakistan"
    tags: list[str] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    related_sections: list[str] = Field(default_factory=list)
    offence_group: str | None = None
    punishment_summary: str | None = None
    provision_kind: str = "general"


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
