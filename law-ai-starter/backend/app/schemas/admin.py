from pydantic import BaseModel


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