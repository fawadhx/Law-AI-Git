from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import desc, func, select
from sqlalchemy.exc import SQLAlchemyError

from app.db.models import LegalSourceVersionORM
from app.db.session import get_database_status, get_session_factory
from app.schemas.admin import AdminDraftFieldChange, AdminSourceHistoryResponse, AdminSourceVersionRecord
from app.schemas.legal_source import LegalSourceRecord
from app.services.admin_audit_service import get_current_admin_audit_context

_FALLBACK_SOURCE_VERSIONS: list[AdminSourceVersionRecord] = []

_TRACKED_FIELDS: tuple[tuple[str, str], ...] = (
    ("source_title", "Source title"),
    ("law_name", "Law name"),
    ("section_number", "Section number"),
    ("section_title", "Section title"),
    ("summary", "Summary"),
    ("excerpt", "Excerpt"),
    ("citation_label", "Citation label"),
    ("jurisdiction", "Jurisdiction"),
    ("jurisdiction_type", "Jurisdiction type"),
    ("government_level", "Government level"),
    ("province", "Province"),
    ("law_category", "Category"),
    ("law_type", "Law type"),
    ("source_status", "Source status"),
    ("official_citation", "Official citation"),
    ("enactment_year", "Enactment year"),
    ("effective_year", "Effective year"),
    ("tags", "Tags"),
    ("aliases", "Aliases"),
    ("keywords", "Keywords"),
    ("related_sections", "Related sections"),
    ("offence_group", "Offence group"),
    ("punishment_summary", "Punishment summary"),
    ("provision_kind", "Provision kind"),
    ("source_url", "Source URL"),
    ("source_last_verified", "Source last verified"),
    ("amendment_notes", "Amendment notes"),
    ("source_trust_level", "Source trust level"),
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _format_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value)


def build_changed_fields(
    before: LegalSourceRecord | None,
    after: LegalSourceRecord | None,
    *,
    action: str,
) -> list[AdminDraftFieldChange]:
    if action == "create" and after is not None:
        return [
            AdminDraftFieldChange(
                field="record",
                label="Record created",
                before=None,
                after=after.citation_label,
                changed=True,
            )
        ]
    if action == "delete" and before is not None:
        return [
            AdminDraftFieldChange(
                field="record",
                label="Record deleted",
                before=before.citation_label,
                after=None,
                changed=True,
            )
        ]

    changes: list[AdminDraftFieldChange] = []
    if before is None or after is None:
        return changes

    for field, label in _TRACKED_FIELDS:
        before_value = _format_value(getattr(before, field, None))
        after_value = _format_value(getattr(after, field, None))
        if before_value == after_value:
            continue
        changes.append(
            AdminDraftFieldChange(
                field=field,
                label=label,
                before=before_value or None,
                after=after_value or None,
                changed=True,
            )
        )
    return changes


def _snapshot(record: LegalSourceRecord | None) -> dict[str, object]:
    if record is None:
        return {}
    return record.model_dump(mode="json")


def _record_from_orm(row: LegalSourceVersionORM) -> AdminSourceVersionRecord:
    created_at = row.created_at.replace(tzinfo=timezone.utc) if row.created_at.tzinfo is None else row.created_at
    changes = [AdminDraftFieldChange(**item) for item in row.changed_fields or []]
    return AdminSourceVersionRecord(
        version_id=row.version_id,
        record_id=row.record_id,
        version_number=row.version_number,
        action=row.action,
        citation_label=row.citation_label,
        title=row.title,
        changed_fields=changes,
        changed_field_count=len(changes),
        actor_username=row.actor_username,
        actor_role=row.actor_role,
        audit_id=row.audit_id,
        created_at=created_at.isoformat(),
    )


def _next_version_number(record_id: str) -> int:
    status_snapshot = get_database_status()
    session_factory = get_session_factory()
    if status_snapshot["ready"] and session_factory is not None:
        try:
            with session_factory() as session:
                current = session.scalar(
                    select(func.max(LegalSourceVersionORM.version_number)).where(
                        LegalSourceVersionORM.record_id == record_id
                    )
                )
            return int(current or 0) + 1
        except SQLAlchemyError:
            pass

    current_fallback = [
        item.version_number for item in _FALLBACK_SOURCE_VERSIONS if item.record_id == record_id
    ]
    return (max(current_fallback) if current_fallback else 0) + 1


def record_legal_source_version(
    *,
    action: str,
    record: LegalSourceRecord,
    before: LegalSourceRecord | None = None,
    audit_id: str | None = None,
) -> AdminSourceVersionRecord:
    created_at = _utc_now()
    context = get_current_admin_audit_context()
    changes = build_changed_fields(before, record, action=action)
    version = AdminSourceVersionRecord(
        version_id=str(uuid4()),
        record_id=record.id,
        version_number=_next_version_number(record.id),
        action=action,
        citation_label=record.citation_label,
        title=record.section_title or record.citation_label,
        changed_fields=changes,
        changed_field_count=len(changes),
        actor_username=context.get("username") or None,
        actor_role=context.get("role") or None,
        audit_id=audit_id,
        created_at=created_at.isoformat(),
    )

    status_snapshot = get_database_status()
    session_factory = get_session_factory()
    if status_snapshot["ready"] and session_factory is not None:
        try:
            with session_factory() as session:
                session.add(
                    LegalSourceVersionORM(
                        version_id=version.version_id,
                        record_id=version.record_id,
                        version_number=version.version_number,
                        action=version.action,
                        citation_label=version.citation_label,
                        title=version.title,
                        changed_fields=[item.model_dump(mode="json") for item in changes],
                        snapshot=_snapshot(record),
                        actor_username=version.actor_username,
                        actor_role=version.actor_role,
                        audit_id=audit_id,
                        created_at=created_at.replace(tzinfo=None),
                    )
                )
                session.commit()
            return version
        except SQLAlchemyError:
            pass

    _FALLBACK_SOURCE_VERSIONS.insert(0, version)
    del _FALLBACK_SOURCE_VERSIONS[200:]
    return version


def record_legal_source_delete_version(
    *,
    record: LegalSourceRecord,
    audit_id: str | None = None,
) -> AdminSourceVersionRecord:
    return record_legal_source_version(action="delete", record=record, before=record, audit_id=audit_id)


def list_legal_source_versions(record_id: str, *, limit: int = 20) -> list[AdminSourceVersionRecord]:
    status_snapshot = get_database_status()
    session_factory = get_session_factory()
    if status_snapshot["ready"] and session_factory is not None:
        try:
            with session_factory() as session:
                rows = session.scalars(
                    select(LegalSourceVersionORM)
                    .where(LegalSourceVersionORM.record_id == record_id)
                    .order_by(desc(LegalSourceVersionORM.version_number))
                    .limit(limit)
                ).all()
            return [_record_from_orm(row) for row in rows]
        except SQLAlchemyError:
            pass

    return [item for item in _FALLBACK_SOURCE_VERSIONS if item.record_id == record_id][:limit]


def list_recent_legal_source_versions(*, limit: int = 30) -> list[AdminSourceVersionRecord]:
    status_snapshot = get_database_status()
    session_factory = get_session_factory()
    if status_snapshot["ready"] and session_factory is not None:
        try:
            with session_factory() as session:
                rows = session.scalars(
                    select(LegalSourceVersionORM).order_by(desc(LegalSourceVersionORM.created_at)).limit(limit)
                ).all()
            return [_record_from_orm(row) for row in rows]
        except SQLAlchemyError:
            pass

    return list(_FALLBACK_SOURCE_VERSIONS[:limit])


def get_legal_source_history(record_id: str, *, limit: int = 20) -> AdminSourceHistoryResponse:
    items = list_legal_source_versions(record_id, limit=limit)
    latest = items[0].version_number if items else None
    return AdminSourceHistoryResponse(
        record_id=record_id,
        total_versions=len(items),
        latest_version_number=latest,
        items=items,
        workflow_note=(
            "Version history starts from the Phase 3 history foundation. Older catalog records may have no prior versions yet."
        ),
    )


def get_recent_legal_source_history(*, limit: int = 30) -> AdminSourceHistoryResponse:
    items = list_recent_legal_source_versions(limit=limit)
    latest = max((item.version_number for item in items), default=None)
    return AdminSourceHistoryResponse(
        record_id=None,
        total_versions=len(items),
        latest_version_number=latest,
        items=items,
        workflow_note="Recent legal-source versions across admin create, update, publish, and delete actions.",
    )
