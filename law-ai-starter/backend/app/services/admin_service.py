from collections import Counter

from app.data.legal_sources import LEGAL_SOURCES
from app.data.officer_authority import OFFICER_AUTHORITY_DATA
from app.schemas.admin import (
    AdminRoadmapItem,
    AdminSourceCatalogResponse,
    AdminSourceCatalogSummary,
    AdminSourceRecord,
    AdminStat,
    AdminStatusCard,
    AdminSummaryResponse,
)
from app.schemas.legal_source import LegalSourceRecord


def _section_sort_key(value: str) -> tuple[int, str]:
    digits = "".join(character for character in value if character.isdigit())
    if digits:
        return (0, digits.zfill(6))
    return (1, value.lower())


def _law_breakdown() -> Counter[str]:
    return Counter(record.law_name for record in LEGAL_SOURCES)


def _group_breakdown() -> Counter[str]:
    return Counter(record.offence_group or "ungrouped" for record in LEGAL_SOURCES)


def _build_admin_note(record: LegalSourceRecord) -> str:
    if record.provision_kind == "procedure":
        return "Procedure-oriented record linked to police or reporting flow."
    if record.provision_kind == "punishment":
        return "Punishment section that pairs with a core offence or conduct definition."
    if record.related_sections:
        return "Structured record linked to companion sections for overlap-aware answers."
    return "Core legal source record available for retrieval and answer composition."


def _build_source_record(record: LegalSourceRecord) -> AdminSourceRecord:
    return AdminSourceRecord(
        id=record.id,
        citation_label=record.citation_label,
        source_title=record.source_title,
        law_name=record.law_name,
        section_number=record.section_number,
        section_title=record.section_title,
        summary=record.summary,
        jurisdiction=record.jurisdiction,
        provision_kind=record.provision_kind,
        offence_group=record.offence_group,
        related_sections=record.related_sections,
        tags=record.tags,
        punishment_summary=record.punishment_summary,
        admin_note=_build_admin_note(record),
    )


def get_admin_summary() -> AdminSummaryResponse:
    total_records = len(LEGAL_SOURCES)
    law_breakdown = _law_breakdown()
    group_breakdown = _group_breakdown()
    punishment_count = sum(1 for record in LEGAL_SOURCES if record.provision_kind == "punishment")

    return AdminSummaryResponse(
        stats=[
            AdminStat(
                value=str(total_records),
                title="Source records",
                description="Structured legal source records currently available to the prototype retrieval layer.",
            ),
            AdminStat(
                value=str(len(law_breakdown)),
                title="Law families",
                description="Distinct laws represented in the current in-memory legal source catalog.",
            ),
            AdminStat(
                value=str(len(group_breakdown)),
                title="Provision groups",
                description="Grouped offence or procedure clusters used for ranking, overlap handling, and answer composition.",
            ),
            AdminStat(
                value=str(len(OFFICER_AUTHORITY_DATA)),
                title="Authority mappings",
                description="Officer-rank summaries and authority notes currently available to the prototype authority layer.",
            ),
        ],
        control_areas=[
            AdminRoadmapItem(
                title="Source catalog",
                text="Browse structured legal records, section pairings, and retrieval-ready metadata from one admin workspace.",
            ),
            AdminRoadmapItem(
                title="Review workflow",
                text="Prepare future draft, review, approval, and archive states for legal source governance.",
            ),
            AdminRoadmapItem(
                title="Authority mappings",
                text="Maintain officer-rank summaries, powers, and limitations with clear legal-information boundaries.",
            ),
            AdminRoadmapItem(
                title="Prompt and policy controls",
                text="Keep future disclaimers, safety guidance, and classification rules centrally managed.",
            ),
        ],
        status_cards=[
            AdminStatusCard(
                title="Source catalog status",
                content=(
                    f"The admin panel is now connected to a live prototype catalog of {total_records} in-memory legal records. "
                    "Editing, approvals, and uploads are still planned rather than implemented."
                ),
            ),
            AdminStatusCard(
                title="Coverage status",
                content=(
                    f"The current catalog spans {len(law_breakdown)} law families and {punishment_count} punishment-oriented sections, "
                    "which is enough for a credible prototype but not yet a full legal corpus."
                ),
            ),
        ],
        workflow_steps=[
            "Review section wording and linked sections before treating a record as production-ready.",
            "Verify that offence, punishment, and procedure sections are paired correctly for answer composition.",
            "Keep legal-information boundaries and disclaimer wording centrally governed before expanding public usage.",
            "Prepare future source editing, publishing, and audit-log controls before any real admin rollout.",
        ],
        roadmap_items=[
            AdminRoadmapItem(
                title="Source detail drawer",
                text="Open one record at a time with full excerpt, companion sections, and future review notes.",
            ),
            AdminRoadmapItem(
                title="Structured editor",
                text="Add or edit legal records from admin without touching code files directly.",
            ),
            AdminRoadmapItem(
                title="Review states",
                text="Move records through draft, reviewed, approved, and archived states with validation rules.",
            ),
            AdminRoadmapItem(
                title="Authority editor",
                text="Maintain officer authority summaries and boundaries alongside legal section references.",
            ),
            AdminRoadmapItem(
                title="Policy manager",
                text="Version disclaimers, retrieval rules, and future safety guidance from a controlled admin layer.",
            ),
            AdminRoadmapItem(
                title="Audit trail",
                text="Track record changes, approvals, and future admin actions before production deployment.",
            ),
        ],
        admin_boundary=(
            "This admin area is still a prototype control surface. It can now inspect the legal source catalog, "
            "but authentication, editing, approvals, uploads, persistence, and audit logging must be added before "
            "it is treated as a real production admin system."
        ),
    )



def get_admin_source_catalog() -> AdminSourceCatalogResponse:
    law_breakdown = _law_breakdown()
    group_breakdown = _group_breakdown()

    items = sorted(
        (_build_source_record(record) for record in LEGAL_SOURCES),
        key=lambda item: (item.law_name.lower(), _section_sort_key(item.section_number), item.section_title.lower()),
    )

    return AdminSourceCatalogResponse(
        summary=AdminSourceCatalogSummary(
            total_records=len(items),
            law_count=len(law_breakdown),
            offence_group_count=len(group_breakdown),
            punishment_record_count=sum(1 for item in items if item.provision_kind == "punishment"),
            procedure_record_count=sum(1 for item in items if item.provision_kind == "procedure"),
        ),
        items=items,
        available_laws=sorted(law_breakdown.keys()),
        available_groups=sorted(group_breakdown.keys()),
        available_kinds=sorted({record.provision_kind for record in LEGAL_SOURCES}),
        workflow_note=(
            "This catalog is read-only for now. In later phases, the same workspace should support add, edit, review, "
            "publish, and archive actions for legal records."
        ),
    )
