from collections import Counter

from app.data.legal_sources import LEGAL_SOURCES
from app.data.officer_authority import OFFICER_AUTHORITY_DATA
from app.schemas.admin import (
    AdminCatalogSourceInfo,
    AdminDraftFieldChange,
    AdminDraftSectionCheck,
    AdminDraftValidationIssue,
    AdminLinkedRecord,
    AdminReviewChecklistItem,
    AdminRoadmapItem,
    AdminSourceCatalogResponse,
    AdminSourceCatalogSummary,
    AdminSourceDetailRecord,
    AdminSourceDetailResponse,
    AdminSourceDraftInput,
    AdminSourceDraftPreview,
    AdminSourceDraftReviewResponse,
    AdminSourceDraftValidationResponse,
    AdminSourcePublishPreviewResponse,
    AdminSourceRecord,
    AdminStat,
    AdminStatusCard,
    AdminSummaryResponse,
    AdminActivityFeedResponse,
    AdminActivityRecord,
    AdminPublishExecutionResponse,
)
from app.schemas.legal_source import LegalSourceRecord
from app.services.legal_source_store import (
    get_legal_source_store_snapshot,
    upsert_persisted_legal_source,
)


def _active_store_snapshot():
    return get_legal_source_store_snapshot()


def _active_records() -> list[LegalSourceRecord]:
    return _active_store_snapshot().records


def _record_index(records: list[LegalSourceRecord] | None = None) -> dict[str, LegalSourceRecord]:
    active = records if records is not None else _active_records()
    return {record.id: record for record in active}


def _known_laws(records: list[LegalSourceRecord] | None = None) -> list[str]:
    active = records if records is not None else _active_records()
    return sorted({record.law_name for record in active})


def _known_kinds(records: list[LegalSourceRecord] | None = None) -> list[str]:
    active = records if records is not None else _active_records()
    return sorted({record.provision_kind for record in active})


def _known_groups(records: list[LegalSourceRecord] | None = None) -> list[str]:
    active = records if records is not None else _active_records()
    return sorted({record.offence_group for record in active if record.offence_group})


def _section_sort_key(value: str) -> tuple[int, str]:
    digits = "".join(character for character in value if character.isdigit())
    if digits:
        return (0, digits.zfill(6))
    return (1, value.lower())


def _clean_list(values: list[str]) -> list[str]:
    seen: set[str] = set()
    cleaned: list[str] = []
    for value in values:
        item = value.strip()
        if not item:
            continue
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        cleaned.append(item)
    return cleaned


def _law_breakdown(records: list[LegalSourceRecord] | None = None) -> Counter[str]:
    active = records if records is not None else _active_records()
    return Counter(record.law_name for record in active)


def _group_breakdown(records: list[LegalSourceRecord] | None = None) -> Counter[str]:
    active = records if records is not None else _active_records()
    return Counter(record.offence_group or "ungrouped" for record in active)


def _slugify(value: str) -> str:
    cleaned = []
    previous_dash = False
    for character in value.lower():
        if character.isalnum():
            cleaned.append(character)
            previous_dash = False
        elif not previous_dash:
            cleaned.append('-')
            previous_dash = True
    slug = ''.join(cleaned).strip('-')
    return slug or 'record'


def _build_record_id(payload: AdminSourceDraftInput) -> str:
    law_part = _slugify(payload.law_name)[:24]
    section_part = _slugify(payload.section_number)[:18]
    title_part = _slugify(payload.section_title)[:24]
    return f"draft-{law_part}-{section_part}-{title_part}-{uuid4().hex[:6]}"


def _sort_live_catalog() -> None:
    LEGAL_SOURCES.sort(
        key=lambda record: (
            record.law_name.lower(),
            _section_sort_key(record.section_number),
            record.section_title.lower(),
            record.id.lower(),
        )
    )


def _draft_to_live_record(payload: AdminSourceDraftInput, record_id: str) -> LegalSourceRecord:
    return LegalSourceRecord(
        id=record_id,
        source_title=payload.source_title,
        law_name=payload.law_name,
        section_number=payload.section_number,
        section_title=payload.section_title,
        summary=payload.summary,
        excerpt=payload.excerpt,
        citation_label=payload.citation_label,
        jurisdiction=payload.jurisdiction,
        tags=list(payload.tags),
        aliases=list(payload.aliases),
        keywords=list(payload.keywords),
        related_sections=list(payload.related_sections),
        offence_group=payload.offence_group,
        punishment_summary=payload.punishment_summary,
        provision_kind=payload.provision_kind,
    )


def _upsert_live_record(payload: AdminSourceDraftInput, target_record_id: str | None = None) -> LegalSourceRecord:
    record_id = target_record_id or payload.id or _build_record_id(payload)
    new_record = _draft_to_live_record(payload, record_id=record_id)
    for index, existing in enumerate(LEGAL_SOURCES):
        if existing.id == record_id:
            LEGAL_SOURCES[index] = new_record
            _sort_live_catalog()
            return new_record
    LEGAL_SOURCES.append(new_record)
    _sort_live_catalog()
    return new_record


def _build_admin_note(record: LegalSourceRecord | AdminSourceDraftInput) -> str:
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


def _companion_records(record: LegalSourceRecord, records: list[LegalSourceRecord]) -> list[AdminLinkedRecord]:
    companions: list[AdminLinkedRecord] = []

    for other in _sort_records(list(records)):
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


def _same_group_records(record: LegalSourceRecord, excluded_ids: set[str], records: list[LegalSourceRecord]) -> list[AdminLinkedRecord]:
    if not record.offence_group:
        return []

    results = [
        _build_linked_record(other, "Same offence group")
        for other in _sort_records(list(records))
        if other.id not in excluded_ids
        and other.id != record.id
        and other.offence_group == record.offence_group
    ]
    return results[:8]


def _same_law_records(record: LegalSourceRecord, excluded_ids: set[str], records: list[LegalSourceRecord]) -> list[AdminLinkedRecord]:
    results = [
        _build_linked_record(other, "Same law family")
        for other in _sort_records(list(records))
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

    deduped_terms = _clean_list(searchable_terms)

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


def _normalize_draft(payload: AdminSourceDraftInput) -> AdminSourceDraftInput:
    law_name = payload.law_name.strip()
    citation_label = payload.citation_label.strip()
    section_number = payload.section_number.strip()

    if not citation_label and law_name and section_number:
        citation_label = f"{law_name} s. {section_number}"

    return AdminSourceDraftInput(
        id=payload.id,
        source_title=payload.source_title.strip(),
        law_name=law_name,
        section_number=section_number,
        section_title=payload.section_title.strip(),
        summary=payload.summary.strip(),
        excerpt=payload.excerpt.strip(),
        citation_label=citation_label,
        jurisdiction=payload.jurisdiction.strip() or "Pakistan",
        tags=_clean_list(payload.tags),
        aliases=_clean_list(payload.aliases),
        keywords=_clean_list(payload.keywords),
        related_sections=_clean_list(payload.related_sections),
        offence_group=(payload.offence_group or "").strip() or None,
        punishment_summary=(payload.punishment_summary or "").strip() or None,
        provision_kind=payload.provision_kind.strip() or "general",
    )


def _related_section_check(payload: AdminSourceDraftInput, records: list[LegalSourceRecord]) -> AdminDraftSectionCheck:
    if not payload.related_sections or not payload.law_name:
        return AdminDraftSectionCheck()

    valid_sections = {
        record.section_number
        for record in records
        if record.law_name == payload.law_name
    }
    existing = [section for section in payload.related_sections if section in valid_sections]
    missing = [section for section in payload.related_sections if section not in valid_sections]
    return AdminDraftSectionCheck(existing=existing, missing=missing)


def _build_draft_preview(payload: AdminSourceDraftInput) -> AdminSourceDraftPreview:
    searchable_terms = _clean_list([
        *payload.aliases,
        *payload.keywords,
        *payload.tags,
        payload.section_number,
        payload.section_title,
        payload.law_name,
        payload.offence_group or "",
    ])

    return AdminSourceDraftPreview(
        citation_label=payload.citation_label,
        law_name=payload.law_name,
        section_number=payload.section_number,
        section_title=payload.section_title,
        provision_kind=payload.provision_kind,
        offence_group=payload.offence_group,
        related_sections=payload.related_sections,
        tags=payload.tags,
        aliases=payload.aliases,
        keywords=payload.keywords,
        searchable_terms=searchable_terms[:20],
        admin_note=_build_admin_note(payload),
    )


def _validate_draft(payload: AdminSourceDraftInput) -> tuple[list[AdminDraftValidationIssue], AdminDraftSectionCheck]:
    active_records = _active_records()
    issues: list[AdminDraftValidationIssue] = []

    def add_issue(field: str, level: str, message: str) -> None:
        issues.append(AdminDraftValidationIssue(field=field, level=level, message=message))

    if not payload.source_title:
        add_issue("source_title", "error", "Source title is required.")
    if not payload.law_name:
        add_issue("law_name", "error", "Law name is required.")
    elif payload.law_name not in _known_laws(active_records):
        add_issue("law_name", "warning", "Law name is not in the current prototype catalog, so linked-section checks will be limited.")
    if not payload.section_number:
        add_issue("section_number", "error", "Section number is required.")
    if not payload.section_title:
        add_issue("section_title", "error", "Section title is required.")
    if not payload.summary:
        add_issue("summary", "error", "Summary is required.")
    elif len(payload.summary) < 50:
        add_issue("summary", "warning", "Summary is very short. Add more plain-language meaning so admin review is easier.")
    if not payload.excerpt:
        add_issue("excerpt", "error", "Excerpt is required.")
    elif len(payload.excerpt) < 80:
        add_issue("excerpt", "warning", "Excerpt looks short for a citation-first answer experience.")

    if payload.provision_kind not in _known_kinds(active_records):
        add_issue("provision_kind", "warning", "Provision kind is not in the current prototype set.")

    if payload.provision_kind == "punishment" and not payload.punishment_summary:
        add_issue("punishment_summary", "warning", "Punishment records should usually include a punishment summary.")

    if payload.provision_kind != "procedure" and not payload.offence_group:
        add_issue("offence_group", "warning", "A non-procedure record usually benefits from an offence group for overlap handling.")

    if len(payload.tags) == 0:
        add_issue("tags", "warning", "Add at least one tag to improve retrieval and admin filtering.")
    if len(payload.aliases) == 0:
        add_issue("aliases", "warning", "No aliases added yet. Real-world user wording may be harder to match.")
    if len(payload.keywords) == 0:
        add_issue("keywords", "warning", "No keywords added yet. Retrieval quality may be weaker.")

    related_section_check = _related_section_check(payload, active_records)
    if related_section_check.missing:
        add_issue(
            "related_sections",
            "warning",
            "Some related sections were not found under the selected law: " + ", ".join(related_section_check.missing),
        )

    if not payload.citation_label:
        add_issue("citation_label", "warning", "Citation label was auto-filled. Review it before using this draft as a baseline.")

    return issues, related_section_check


def _build_catalog_source_info():
    snapshot = _active_store_snapshot()
    return AdminCatalogSourceInfo(
        active_source=snapshot.active_source,
        source_label=snapshot.source_label,
        database_ready=snapshot.database_ready,
        foundation_stage=snapshot.foundation_stage,
        active_record_count=snapshot.active_record_count,
        persisted_record_count=snapshot.persisted_record_count,
        detail=snapshot.detail,
    )


def get_admin_summary() -> AdminSummaryResponse:
    snapshot = _active_store_snapshot()
    active_records = snapshot.records
    total_records = len(active_records)
    law_breakdown = _law_breakdown(active_records)
    group_breakdown = _group_breakdown(active_records)
    punishment_count = sum(1 for record in active_records if record.provision_kind == "punishment")

    db_mode_value = "Connected" if snapshot.database_ready else "In memory"
    persisted_value = str(snapshot.persisted_record_count)
    foundation_stage = snapshot.foundation_stage.replace("_", " ")

    return AdminSummaryResponse(
        stats=[
            AdminStat(
                value=str(total_records),
                title="Source records",
                description=(
                    "Structured legal source records currently visible to admin from the active catalog source."
                ),
            ),
            AdminStat(
                value=str(len(law_breakdown)),
                title="Law families",
                description="Distinct laws represented in the active admin source catalog.",
            ),
            AdminStat(
                value=db_mode_value,
                title="Database mode",
                description="Shows whether the Phase 5 foundation is still running in memory or connected to PostgreSQL.",
            ),
            AdminStat(
                value=persisted_value,
                title="Persisted records",
                description="Legal source rows currently present in the database foundation table when the database is available.",
            ),
            AdminStat(
                value=snapshot.source_label,
                title="Active catalog source",
                description="Shows whether admin is reading from the persisted database catalog or the in-memory prototype fallback.",
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
                title="Draft editor",
                text="Edit a working draft safely, validate fields, and preview readiness without changing the live prototype dataset.",
            ),
            AdminRoadmapItem(
                title="Database-backed source reading",
                text="Let admin prefer persisted PostgreSQL records when they exist while still falling back safely to the in-memory prototype catalog.",
            ),
        ],
        status_cards=[
            AdminStatusCard(
                title="Source catalog status",
                content=(
                    f"Admin is currently using {snapshot.source_label.lower()} with {total_records} active record(s). "
                    "Record inspection, draft validation, workspace shelving, and controlled session publish are available while database-backed retrieval is being introduced in Phase 5."
                ),
            ),
            AdminStatusCard(
                title="Database foundation",
                content=(
                    f"Current foundation stage: {foundation_stage}. {snapshot.detail} "
                    f"The current persisted row count is {persisted_value}."
                ),
            ),
            AdminStatusCard(
                title="Coverage status",
                content=(
                    f"The active catalog spans {len(law_breakdown)} law families, {len(group_breakdown)} provision groups, and {punishment_count} punishment-oriented sections, "
                    "which is enough for a credible prototype but not yet a full legal corpus."
                ),
            ),
        ],
        workflow_steps=[
            "Keep the in-memory catalog as the fallback baseline while PostgreSQL-backed admin reads are introduced safely.",
            "Review section wording, excerpt quality, and linked sections before treating a record as production-ready.",
            "Validate a working draft, then save it into the workspace shelf before moving it toward publish review.",
            "Prepare future retrieval migration, approvals, and audit-log controls before any real admin rollout.",
        ],
        roadmap_items=[
            AdminRoadmapItem(
                title="Database read path",
                text="Prefer persisted legal source records in admin views when the database is ready and seeded.",
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
                title="Audit trail",
                text="Track record changes, approvals, and future admin actions before production deployment.",
            ),
        ],
        admin_boundary=(
            "This admin area is still a prototype control surface. It can inspect the legal source catalog, open detailed source views, validate working drafts, stage prototype publish actions, and now prefer persisted database records when they exist, "
            "but authentication, durable approvals, uploads, and production-grade audit logging must be added before it is treated as a real admin system."
        ),
        catalog_source=_build_catalog_source_info(),
    )


def get_admin_source_catalog() -> AdminSourceCatalogResponse:
    snapshot = _active_store_snapshot()
    active_records = snapshot.records
    law_breakdown = _law_breakdown(active_records)
    group_breakdown = _group_breakdown(active_records)

    items = sorted(
        (_build_source_record(record) for record in active_records),
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
        catalog_source=_build_catalog_source_info(),
        items=items,
        available_laws=sorted(law_breakdown.keys()),
        available_groups=sorted(group_breakdown.keys()),
        available_kinds=sorted({record.provision_kind for record in active_records}),
        workflow_note=(
            "This catalog is still read-only, but admin can now prefer persisted database records when PostgreSQL is ready and seeded, while still falling back safely to the in-memory prototype catalog. "
            "The detail view, draft validation workflow, and session publish tools remain available on top of that active source."
        ),
    )


def get_admin_source_detail(source_id: str) -> AdminSourceDetailResponse | None:
    snapshot = _active_store_snapshot()
    active_records = snapshot.records
    record = _record_index(active_records).get(source_id)
    if record is None:
        return None

    companion_records = _companion_records(record, active_records)
    excluded_ids = {linked.id for linked in companion_records}
    same_group_records = _same_group_records(record, excluded_ids, active_records)
    excluded_ids.update(linked.id for linked in same_group_records)
    same_law_records = _same_law_records(record, excluded_ids, active_records)

    return AdminSourceDetailResponse(
        item=_detail_record(record, companion_records, same_group_records, same_law_records),
        catalog_source=_build_catalog_source_info(),
        companion_records=companion_records,
        same_group_records=same_group_records,
        same_law_records=same_law_records,
        workflow_note=(
            "Use this detail view to validate excerpt quality, searchable wording, and section pairings. "
            "When PostgreSQL is seeded, this panel now reads from the persisted source catalog instead of only the in-memory prototype list."
        ),
    )


def validate_admin_source_draft(payload: AdminSourceDraftInput) -> AdminSourceDraftValidationResponse:
    normalized = _normalize_draft(payload)
    issues, related_section_check = _validate_draft(normalized)
    error_count = sum(1 for issue in issues if issue.level == "error")
    warning_count = sum(1 for issue in issues if issue.level == "warning")
    readiness_score = max(0, min(100, 100 - error_count * 18 - warning_count * 6))

    return AdminSourceDraftValidationResponse(
        preview=_build_draft_preview(normalized),
        readiness_score=readiness_score,
        issue_count=len(issues),
        error_count=error_count,
        warning_count=warning_count,
        issues=issues,
        related_section_check=related_section_check,
        workflow_note=(
            "This validation flow checks draft completeness and relationship hygiene without changing the live in-memory catalog. "
            "Treat it as a preparation step before future real save, review, and publish workflows are added."
        ),
    )


FIELD_LABELS = {
    "source_title": "Source title",
    "law_name": "Law name",
    "section_number": "Section number",
    "section_title": "Section title",
    "summary": "Summary",
    "excerpt": "Excerpt",
    "citation_label": "Citation label",
    "jurisdiction": "Jurisdiction",
    "provision_kind": "Provision kind",
    "offence_group": "Offence group",
    "punishment_summary": "Punishment summary",
    "tags": "Tags",
    "aliases": "Aliases",
    "keywords": "Keywords",
    "related_sections": "Related sections",
}

REQUIRED_REVIEW_FIELDS = {
    "source_title",
    "law_name",
    "section_number",
    "section_title",
    "summary",
    "excerpt",
}


def _stringify_change_value(value: str | list[str] | None) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(value)
    return value


def _record_to_draft(record: LegalSourceRecord) -> AdminSourceDraftInput:
    return AdminSourceDraftInput(
        id=record.id,
        source_title=record.source_title,
        law_name=record.law_name,
        section_number=record.section_number,
        section_title=record.section_title,
        summary=record.summary,
        excerpt=record.excerpt,
        citation_label=record.citation_label,
        jurisdiction=record.jurisdiction,
        tags=list(record.tags),
        aliases=list(record.aliases),
        keywords=list(record.keywords),
        related_sections=list(record.related_sections),
        offence_group=record.offence_group,
        punishment_summary=record.punishment_summary,
        provision_kind=record.provision_kind,
    )


def _empty_draft_baseline() -> AdminSourceDraftInput:
    return AdminSourceDraftInput(
        source_title="",
        law_name="",
        section_number="",
        section_title="",
        summary="",
        excerpt="",
        citation_label="",
        jurisdiction="Pakistan",
        tags=[],
        aliases=[],
        keywords=[],
        related_sections=[],
        offence_group=None,
        punishment_summary=None,
        provision_kind="general",
    )


def _compare_draft_fields(payload: AdminSourceDraftInput, existing_record: LegalSourceRecord | None) -> list[AdminDraftFieldChange]:
    baseline = _record_to_draft(existing_record) if existing_record else _empty_draft_baseline()
    changes: list[AdminDraftFieldChange] = []

    for field, label in FIELD_LABELS.items():
        before_value = _stringify_change_value(getattr(baseline, field))
        after_value = _stringify_change_value(getattr(payload, field))
        changed = before_value != after_value
        if not changed and existing_record is not None:
            continue
        if not changed and not after_value and existing_record is None:
            continue
        changes.append(
            AdminDraftFieldChange(
                field=field,
                label=label,
                before=before_value or None,
                after=after_value or None,
                changed=changed,
            )
        )

    return changes


def _collect_issue_messages(issues: list[AdminDraftValidationIssue], *, level: str | None = None, fields: set[str] | None = None) -> list[str]:
    collected: list[str] = []
    for issue in issues:
        if level and issue.level != level:
            continue
        if fields and issue.field not in fields:
            continue
        collected.append(issue.message)
    return collected


def _status_from_issues(blockers: list[str], warnings: list[str]) -> str:
    if blockers:
        return "block"
    if warnings:
        return "warning"
    return "pass"


def _build_review_checklist(
    payload: AdminSourceDraftInput,
    issues: list[AdminDraftValidationIssue],
    related_section_check: AdminDraftSectionCheck,
    changed_fields: list[AdminDraftFieldChange],
) -> list[AdminReviewChecklistItem]:
    retrieval_fields = {"tags", "aliases", "keywords"}
    relationship_fields = {"related_sections"}
    pairing_fields = {"offence_group", "punishment_summary", "provision_kind"}
    context_fields = {"law_name"}

    core_blockers = _collect_issue_messages(issues, level="error", fields=REQUIRED_REVIEW_FIELDS)
    core_warnings = _collect_issue_messages(issues, level="warning", fields=REQUIRED_REVIEW_FIELDS)
    retrieval_warnings = _collect_issue_messages(issues, level="warning", fields=retrieval_fields)
    relationship_warnings = _collect_issue_messages(issues, level="warning", fields=relationship_fields)
    pairing_warnings = _collect_issue_messages(issues, level="warning", fields=pairing_fields)
    context_warnings = _collect_issue_messages(issues, level="warning", fields=context_fields)

    change_detail = (
        f"{len(changed_fields)} changed field(s) detected against the live catalog record."
        if payload.id
        else f"{len(changed_fields)} populated field(s) prepared for a new record draft."
    )
    if payload.id and len(changed_fields) == 0:
        change_detail = "No field changes were detected against the selected live record."

    return [
        AdminReviewChecklistItem(
            key="core_fields",
            title="Core field completeness",
            status=_status_from_issues(core_blockers, core_warnings),
            detail=(
                "; ".join(core_blockers or core_warnings)
                if (core_blockers or core_warnings)
                else "Core section identity, summary, and excerpt fields are present."
            ),
        ),
        AdminReviewChecklistItem(
            key="retrieval_metadata",
            title="Retrieval metadata strength",
            status=_status_from_issues([], retrieval_warnings),
            detail=(
                "; ".join(retrieval_warnings)
                if retrieval_warnings
                else "Tags, aliases, and keywords look usable for prototype retrieval and admin filtering."
            ),
        ),
        AdminReviewChecklistItem(
            key="section_relationships",
            title="Section relationship hygiene",
            status=_status_from_issues([], relationship_warnings),
            detail=(
                "; ".join(relationship_warnings)
                if relationship_warnings
                else (
                    f"{len(related_section_check.existing)} linked section(s) confirmed under the selected law."
                    if related_section_check.existing
                    else "No broken related-section links detected in the current draft."
                )
            ),
        ),
        AdminReviewChecklistItem(
            key="kind_pairing",
            title="Provision kind pairing",
            status=_status_from_issues([], pairing_warnings),
            detail=(
                "; ".join(pairing_warnings)
                if pairing_warnings
                else "Provision kind, offence grouping, and punishment-pairing signals look internally consistent."
            ),
        ),
        AdminReviewChecklistItem(
            key="catalog_context",
            title="Catalog context fit",
            status=_status_from_issues([], context_warnings),
            detail=(
                "; ".join(context_warnings)
                if context_warnings
                else "The draft fits the current prototype catalog context and can be reviewed against same-law records."
            ),
        ),
        AdminReviewChecklistItem(
            key="change_scope",
            title="Change scope",
            status=("warning" if payload.id and len(changed_fields) == 0 else "pass"),
            detail=change_detail,
        ),
    ]


def _context_counts(payload: AdminSourceDraftInput) -> tuple[int, int, int]:
    active_records = _active_records()
    companion_hit_count = sum(
        1
        for record in active_records
        if record.law_name == payload.law_name and record.section_number in payload.related_sections
    )
    same_group_context_count = sum(
        1 for record in active_records if payload.offence_group and record.offence_group == payload.offence_group
    )
    same_law_context_count = sum(1 for record in active_records if record.law_name == payload.law_name)
    return companion_hit_count, same_group_context_count, same_law_context_count


def review_admin_source_draft(payload: AdminSourceDraftInput) -> AdminSourceDraftReviewResponse:
    normalized = _normalize_draft(payload)
    issues, related_section_check = _validate_draft(normalized)
    active_records = _active_records()
    existing_record = _record_index(active_records).get(normalized.id) if normalized.id else None
    changed_fields = _compare_draft_fields(normalized, existing_record)
    checklist = _build_review_checklist(normalized, issues, related_section_check, changed_fields)

    blocker_count = sum(1 for issue in issues if issue.level == "error")
    warning_count = sum(1 for issue in issues if issue.level == "warning")
    publish_mode = "update_existing_record" if existing_record else "create_new_record"

    if blocker_count > 0:
        review_status = "blocked"
        approval_label = "Blocked before publish preview"
    elif warning_count > 0 or (existing_record is not None and len(changed_fields) == 0):
        review_status = "needs_review"
        approval_label = "Needs reviewer attention"
    else:
        review_status = "ready"
        approval_label = "Ready for publish preview"

    readiness_score = max(0, min(100, 100 - blocker_count * 18 - warning_count * 6 - (0 if changed_fields else 4)))

    return AdminSourceDraftReviewResponse(
        review_status=review_status,
        approval_label=approval_label,
        readiness_score=readiness_score,
        blocker_count=blocker_count,
        warning_count=warning_count,
        publish_mode=publish_mode,
        changed_field_count=sum(1 for item in changed_fields if item.changed),
        changed_fields=[item for item in changed_fields if item.changed],
        checklist=checklist,
        workflow_note=(
            "This review gate is still prototype-only. It compares the working draft against the active live record from the current admin source store, surfaces blockers and review warnings, and prepares the draft for a later real approval or publish workflow without persisting any change yet."
        ),
    )


def build_admin_source_publish_preview(payload: AdminSourceDraftInput) -> AdminSourcePublishPreviewResponse:
    normalized = _normalize_draft(payload)
    issues, _related_section_check = _validate_draft(normalized)
    active_records = _active_records()
    existing_record = _record_index(active_records).get(normalized.id) if normalized.id else None
    changed_fields = _compare_draft_fields(normalized, existing_record)
    blocker_messages = _collect_issue_messages(issues, level="error")
    warning_messages = _collect_issue_messages(issues, level="warning")

    if existing_record is not None and not any(item.changed for item in changed_fields):
        warning_messages.append("No changed fields were detected against the selected live record.")

    searchable_term_count = len(_build_draft_preview(normalized).searchable_terms)
    companion_hit_count, same_group_context_count, same_law_context_count = _context_counts(normalized)
    linked_section_count = len(normalized.related_sections)

    recommended_actions: list[str] = []
    if blocker_messages:
        recommended_actions.append("Resolve validation blockers before attempting a real save or publish workflow.")
    if any(issue.field in {"tags", "aliases", "keywords"} for issue in issues if issue.level == "warning"):
        recommended_actions.append("Strengthen aliases, keywords, and tags so retrieval quality does not regress after publishing.")
    if any(issue.field == "related_sections" for issue in issues if issue.level == "warning"):
        recommended_actions.append("Review broken related sections so overlap handling remains trustworthy.")
    if normalized.provision_kind == "punishment" and not normalized.punishment_summary:
        recommended_actions.append("Add a clearer punishment summary so admin reviewers can see the pairing intent quickly.")
    if not recommended_actions:
        recommended_actions.append("Use this publish preview as the final handoff artifact before persistence and approval states are added.")

    return AdminSourcePublishPreviewResponse(
        publish_status=("blocked" if blocker_messages else "preview_ready"),
        publish_mode=("update_existing_record" if existing_record else "create_new_record"),
        target_record_id=existing_record.id if existing_record else (normalized.id or None),
        changed_field_count=sum(1 for item in changed_fields if item.changed),
        searchable_term_count=searchable_term_count,
        linked_section_count=linked_section_count,
        companion_hit_count=companion_hit_count,
        same_group_context_count=same_group_context_count,
        same_law_context_count=same_law_context_count,
        blockers=blocker_messages,
        warnings=warning_messages,
        recommended_actions=recommended_actions,
        changed_fields=[item for item in changed_fields if item.changed],
        workflow_note=(
            "This publish preview does not mutate the live catalog. It estimates how the draft would land inside the current admin source store so an admin can review impact, context, and remaining risks before full persistence workflows exist."
        ),
    )


from datetime import UTC, datetime
from uuid import uuid4

from app.schemas.admin import (
    AdminPublishQueueRecord,
    AdminWorkspaceDraftDetailResponse,
    AdminWorkspaceDraftRecord,
    AdminWorkspaceDraftSaveRequest,
    AdminWorkspaceResponse,
    AdminWorkspaceStageRequest,
    AdminActivityFeedResponse,
    AdminActivityRecord,
    AdminPublishExecutionResponse,
)

WORKSPACE_DRAFT_STORE: dict[str, dict] = {}
PUBLISH_PACKAGE_STORE: dict[str, dict] = {}
ACTIVITY_FEED_STORE: list[AdminActivityRecord] = []


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _title_from_draft(payload: AdminSourceDraftInput, explicit_label: str | None = None) -> str:
    if explicit_label and explicit_label.strip():
        return explicit_label.strip()
    if payload.citation_label:
        return payload.citation_label
    if payload.law_name and payload.section_number:
        return f"{payload.law_name} s. {payload.section_number}"
    if payload.section_title:
        return payload.section_title
    return "Untitled workspace draft"


def _build_workspace_draft_record(
    *,
    workspace_draft_id: str,
    title: str,
    payload: AdminSourceDraftInput,
    validation: AdminSourceDraftValidationResponse,
    review: AdminSourceDraftReviewResponse,
    publish_preview: AdminSourcePublishPreviewResponse,
    version: int,
    saved_at: str,
) -> AdminWorkspaceDraftRecord:
    return AdminWorkspaceDraftRecord(
        workspace_draft_id=workspace_draft_id,
        title=title,
        citation_label=validation.preview.citation_label,
        law_name=validation.preview.law_name,
        section_number=validation.preview.section_number,
        publish_mode=review.publish_mode,
        source_record_id=payload.id,
        version=version,
        readiness_score=review.readiness_score,
        review_status=review.review_status,
        publish_status=publish_preview.publish_status,
        blocker_count=review.blocker_count,
        warning_count=review.warning_count,
        changed_field_count=review.changed_field_count,
        saved_at=saved_at,
    )


def _workspace_detail_response(entry: dict) -> AdminWorkspaceDraftDetailResponse:
    return AdminWorkspaceDraftDetailResponse(
        workspace_draft=entry["workspace_draft"],
        payload=entry["payload"],
        validation=entry["validation"],
        review=entry["review"],
        publish_preview=entry["publish_preview"],
        workflow_note=(
            "Workspace drafts are stored only in prototype server memory for this session. "
            "They let you save draft snapshots, reopen them, and prepare staged publish packages without mutating the live catalog."
        ),
    )


def _sorted_workspace_drafts() -> list[AdminWorkspaceDraftRecord]:
    items = [entry["workspace_draft"] for entry in WORKSPACE_DRAFT_STORE.values()]
    return sorted(items, key=lambda item: item.saved_at, reverse=True)


def _sorted_publish_packages() -> list[AdminPublishQueueRecord]:
    items = [entry["publish_package"] for entry in PUBLISH_PACKAGE_STORE.values()]
    return sorted(items, key=lambda item: item.staged_at, reverse=True)


def get_admin_workspace() -> AdminWorkspaceResponse:
    drafts = _sorted_workspace_drafts()
    publish_queue = _sorted_publish_packages()
    ready_draft_count = sum(1 for item in drafts if item.review_status == "ready")
    blocked_item_count = sum(1 for item in drafts if item.review_status == "blocked") + sum(
        1 for item in publish_queue if item.publish_status == "blocked"
    )
    return AdminWorkspaceResponse(
        saved_draft_count=len(drafts),
        staged_publish_count=len(publish_queue),
        ready_draft_count=ready_draft_count,
        blocked_item_count=blocked_item_count,
        session_publish_count=sum(1 for item in ACTIVITY_FEED_STORE if item.kind == "publish"),
        drafts=drafts,
        publish_queue=publish_queue,
        workflow_note=(
            "This workspace shelf is still prototype-only and resets when the server restarts. "
            "Use it to save draft snapshots, reopen them for editing, and stage publish packages for review before real persistence exists."
        ),
    )


def save_admin_workspace_draft(request: AdminWorkspaceDraftSaveRequest) -> AdminWorkspaceDraftDetailResponse:
    normalized = _normalize_draft(request.draft)
    validation = validate_admin_source_draft(normalized)
    review = review_admin_source_draft(normalized)
    publish_preview = build_admin_source_publish_preview(normalized)

    workspace_draft_id = request.workspace_draft_id or str(uuid4())
    existing_entry = WORKSPACE_DRAFT_STORE.get(workspace_draft_id)
    version = (existing_entry["workspace_draft"].version + 1) if existing_entry else 1
    saved_at = _utc_now_iso()
    title = _title_from_draft(normalized, request.label)

    record = _build_workspace_draft_record(
        workspace_draft_id=workspace_draft_id,
        title=title,
        payload=normalized,
        validation=validation,
        review=review,
        publish_preview=publish_preview,
        version=version,
        saved_at=saved_at,
    )
    WORKSPACE_DRAFT_STORE[workspace_draft_id] = {
        "workspace_draft": record,
        "payload": normalized,
        "validation": validation,
        "review": review,
        "publish_preview": publish_preview,
    }
    return _workspace_detail_response(WORKSPACE_DRAFT_STORE[workspace_draft_id])


def get_admin_workspace_draft(workspace_draft_id: str) -> AdminWorkspaceDraftDetailResponse | None:
    entry = WORKSPACE_DRAFT_STORE.get(workspace_draft_id)
    if entry is None:
        return None
    return _workspace_detail_response(entry)


def delete_admin_workspace_draft(workspace_draft_id: str) -> bool:
    if workspace_draft_id not in WORKSPACE_DRAFT_STORE:
        return False
    del WORKSPACE_DRAFT_STORE[workspace_draft_id]
    orphaned_package_ids = [
        package_id
        for package_id, entry in PUBLISH_PACKAGE_STORE.items()
        if entry["publish_package"].workspace_draft_id == workspace_draft_id
    ]
    for package_id in orphaned_package_ids:
        del PUBLISH_PACKAGE_STORE[package_id]
    return True


def build_admin_workspace_publish_package(request: AdminWorkspaceStageRequest) -> AdminPublishQueueRecord:
    normalized = _normalize_draft(request.draft)
    review = review_admin_source_draft(normalized)
    publish_preview = build_admin_source_publish_preview(normalized)
    validation = validate_admin_source_draft(normalized)

    workspace_draft_id = request.workspace_draft_id
    linked_entry = WORKSPACE_DRAFT_STORE.get(workspace_draft_id) if workspace_draft_id else None
    title = linked_entry["workspace_draft"].title if linked_entry else _title_from_draft(normalized)

    package = AdminPublishQueueRecord(
        package_id=str(uuid4()),
        workspace_draft_id=workspace_draft_id,
        title=title,
        citation_label=validation.preview.citation_label,
        publish_mode=publish_preview.publish_mode,
        target_record_id=publish_preview.target_record_id,
        review_status=review.review_status,
        publish_status=publish_preview.publish_status,
        blocker_count=review.blocker_count,
        warning_count=review.warning_count,
        changed_field_count=publish_preview.changed_field_count,
        staged_at=_utc_now_iso(),
        summary_line=(
            f"{publish_preview.publish_mode.replace('_', ' ')} package for {validation.preview.citation_label or title}. "
            f"{review.blocker_count} blocker(s), {review.warning_count} warning(s), {publish_preview.changed_field_count} changed field(s)."
        ),
    )
    PUBLISH_PACKAGE_STORE[package.package_id] = {
        "publish_package": package,
        "payload": normalized,
        "review": review,
        "publish_preview": publish_preview,
    }
    return package


def delete_admin_workspace_publish_package(package_id: str) -> bool:
    if package_id not in PUBLISH_PACKAGE_STORE:
        return False
    del PUBLISH_PACKAGE_STORE[package_id]
    return True


def _log_activity(*, kind: str, title: str, detail: str, status: str, citation_label: str | None = None, record_id: str | None = None) -> AdminActivityRecord:
    activity = AdminActivityRecord(
        activity_id=str(uuid4()),
        kind=kind,
        title=title,
        detail=detail,
        status=status,
        citation_label=citation_label,
        record_id=record_id,
        created_at=_utc_now_iso(),
    )
    ACTIVITY_FEED_STORE.insert(0, activity)
    del ACTIVITY_FEED_STORE[24:]
    return activity


def get_admin_activity_feed() -> AdminActivityFeedResponse:
    latest_publish = next((item for item in ACTIVITY_FEED_STORE if item.kind == "publish"), None)
    return AdminActivityFeedResponse(
        total_events=len(ACTIVITY_FEED_STORE),
        publish_event_count=sum(1 for item in ACTIVITY_FEED_STORE if item.kind == "publish"),
        latest_publish_label=latest_publish.citation_label if latest_publish else None,
        items=list(ACTIVITY_FEED_STORE),
        workflow_note=(
            "This activity feed is session-only and exists to show prototype publish actions and live-catalog changes during the current server run. "
            "It is helpful for testing, but it is not a real audit log yet."
        ),
    )


def publish_admin_workspace_package(package_id: str) -> AdminPublishExecutionResponse | None:
    package_entry = PUBLISH_PACKAGE_STORE.get(package_id)
    if package_entry is None:
        return None

    package = package_entry["publish_package"]
    if package.publish_status == "blocked" or package.blocker_count > 0:
        raise ValueError("This staged package still has blockers and cannot be published into the live session catalog.")

    payload: AdminSourceDraftInput = _normalize_draft(package_entry["payload"])
    target_record_id = package.target_record_id if package.publish_mode == "update_existing_record" else None
    published_record = _upsert_live_record(payload, target_record_id=target_record_id)
    persisted_sync_applied = upsert_persisted_legal_source(published_record)

    activity = _log_activity(
        kind="publish",
        title=("Published live record update" if package.publish_mode == "update_existing_record" else "Published new live record"),
        detail=(
            f"{package.publish_mode.replace('_', ' ')} applied to {published_record.citation_label}. "
            f"{package.changed_field_count} changed field(s) carried into the live in-memory catalog for this session."
        ),
        status="published",
        citation_label=published_record.citation_label,
        record_id=published_record.id,
    )

    if package.workspace_draft_id and package.workspace_draft_id in WORKSPACE_DRAFT_STORE:
        workspace_entry = WORKSPACE_DRAFT_STORE[package.workspace_draft_id]
        workspace_record: AdminWorkspaceDraftRecord = workspace_entry["workspace_draft"]
        workspace_entry["workspace_draft"] = workspace_record.model_copy(
            update={
                "source_record_id": published_record.id,
                "publish_status": "published_in_session",
            }
        )

    del PUBLISH_PACKAGE_STORE[package_id]

    return AdminPublishExecutionResponse(
        publish_status="published_in_session",
        package_id=package_id,
        published_record_id=published_record.id,
        citation_label=published_record.citation_label,
        publish_mode=package.publish_mode,
        changed_field_count=package.changed_field_count,
        catalog_record_count=len(_active_records()),
        activity=activity,
        workflow_note=(
            "This publish action updated the live in-memory source catalog for the current server session, so admin summary, source catalog, and source detail views can refresh immediately. "
            "It is still not database-backed persistence or a production-grade approval flow."
        ),
    )
