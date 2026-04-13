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
