from collections import Counter

from app.data.legal_sources import LEGAL_SOURCES
from app.data.officer_authority import OFFICER_AUTHORITY_DATA
from app.schemas.admin import (
    AdminLinkedRecord,
    AdminRoadmapItem,
    AdminSourceCatalogResponse,
    AdminSourceCatalogSummary,
    AdminSourceDetailRecord,
    AdminSourceDetailResponse,
    AdminSourceRecord,
    AdminStat,
    AdminStatusCard,
    AdminSummaryResponse,
)
from app.schemas.legal_source import LegalSourceRecord


RECORD_INDEX = {record.id: record for record in LEGAL_SOURCES}


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
        return "Procedure-oriented record linked to police, FIR, arrest, or reporting flow."
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


def _build_linked_record(record: LegalSourceRecord, relationship_label: str) -> AdminLinkedRecord:
    return AdminLinkedRecord(
        id=record.id,
        citation_label=record.citation_label,
        law_name=record.law_name,
        section_number=record.section_number,
        section_title=record.section_title,
        provision_kind=record.provision_kind,
        relationship_label=relationship_label,
        summary=record.summary,
    )


def _sort_records(records: list[LegalSourceRecord]) -> list[LegalSourceRecord]:
    return sorted(
        records,
        key=lambda record: (
            record.law_name.lower(),
            _section_sort_key(record.section_number),
            record.section_title.lower(),
        ),
    )


def _dedupe_linked_records(items: list[AdminLinkedRecord]) -> list[AdminLinkedRecord]:
    seen: set[str] = set()
    deduped: list[AdminLinkedRecord] = []
    for item in items:
        if item.id in seen:
            continue
        seen.add(item.id)
        deduped.append(item)
    return deduped


def _companion_records(record: LegalSourceRecord) -> list[AdminLinkedRecord]:
    companions: list[AdminLinkedRecord] = []

    for other in _sort_records(list(LEGAL_SOURCES)):
        if other.id == record.id:
            continue

        direct_link = (
            other.law_name == record.law_name
            and (other.section_number in record.related_sections or record.section_number in other.related_sections)
        )
        paired_group = (
            bool(record.offence_group)
            and other.law_name == record.law_name
            and other.offence_group == record.offence_group
            and other.provision_kind != record.provision_kind
        )

        if direct_link:
            companions.append(_build_linked_record(other, "Linked section"))
        elif paired_group:
            companions.append(_build_linked_record(other, "Same-group pairing"))

    return _dedupe_linked_records(companions)[:8]


def _same_group_records(record: LegalSourceRecord, excluded_ids: set[str]) -> list[AdminLinkedRecord]:
    if not record.offence_group:
        return []

    results = [
        _build_linked_record(other, "Same offence group")
        for other in _sort_records(list(LEGAL_SOURCES))
        if other.id not in excluded_ids
        and other.id != record.id
        and other.offence_group == record.offence_group
    ]
    return results[:8]


def _same_law_records(record: LegalSourceRecord, excluded_ids: set[str]) -> list[AdminLinkedRecord]:
    results = [
        _build_linked_record(other, "Same law family")
        for other in _sort_records(list(LEGAL_SOURCES))
        if other.id not in excluded_ids
        and other.id != record.id
        and other.law_name == record.law_name
    ]
    return results[:8]


def _detail_record(
    record: LegalSourceRecord,
    companion_records: list[AdminLinkedRecord],
    same_group_records: list[AdminLinkedRecord],
    same_law_records: list[AdminLinkedRecord],
) -> AdminSourceDetailRecord:
    searchable_terms = [
        *record.aliases,
        *record.keywords,
        *record.tags,
    ]

    deduped_terms: list[str] = []
    seen_terms: set[str] = set()
    for term in searchable_terms:
        cleaned = term.strip()
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if lowered in seen_terms:
            continue
        seen_terms.add(lowered)
        deduped_terms.append(cleaned)

    return AdminSourceDetailRecord(
        **_build_source_record(record).model_dump(),
        excerpt=record.excerpt,
        aliases=record.aliases,
        keywords=record.keywords,
        searchable_terms=deduped_terms[:18],
        related_record_count=len(companion_records),
        same_group_record_count=len(same_group_records),
        same_law_record_count=len(same_law_records),
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
                title="Source detail",
                text="Inspect one record deeply with excerpt, keywords, aliases, linked sections, and same-group context.",
            ),
            AdminRoadmapItem(
                title="Review workflow",
                text="Prepare future draft, review, approval, and archive states for legal source governance.",
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
                    "Record inspection is now deeper, but editing, approvals, and uploads are still planned rather than implemented."
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
            "Review section wording, excerpt quality, and linked sections before treating a record as production-ready.",
            "Verify that offence, punishment, and procedure sections are paired correctly for answer composition.",
            "Check aliases, keywords, and searchable terms to keep retrieval behavior grounded in real user wording.",
            "Prepare future source editing, publishing, and audit-log controls before any real admin rollout.",
        ],
        roadmap_items=[
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
            "This admin area is still a prototype control surface. It can inspect the legal source catalog and open detailed source views, "
            "but authentication, editing, approvals, uploads, persistence, and audit logging must be added before it is treated as a real production admin system."
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
            "This catalog is still read-only, but it now supports a detail workflow so one record can be inspected deeply before future edit, review, publish, and archive actions are added."
        ),
    )



def get_admin_source_detail(source_id: str) -> AdminSourceDetailResponse | None:
    record = RECORD_INDEX.get(source_id)
    if record is None:
        return None

    companion_records = _companion_records(record)
    excluded_ids = {linked.id for linked in companion_records}
    same_group_records = _same_group_records(record, excluded_ids)
    excluded_ids.update(linked.id for linked in same_group_records)
    same_law_records = _same_law_records(record, excluded_ids)

    return AdminSourceDetailResponse(
        item=_detail_record(record, companion_records, same_group_records, same_law_records),
        companion_records=companion_records,
        same_group_records=same_group_records,
        same_law_records=same_law_records,
        workflow_note=(
            "Use this detail view to validate excerpt quality, searchable wording, and section pairings before future draft, review, and publish workflows are added."
        ),
    )
