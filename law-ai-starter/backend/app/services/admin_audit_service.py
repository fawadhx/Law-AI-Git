from __future__ import annotations

from contextvars import ContextVar
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import desc, func, select
from sqlalchemy.exc import SQLAlchemyError

from app.db.models import AdminAuditEventORM
from app.db.session import get_database_status, get_session_factory
from app.schemas.admin import AdminActivityRecord
from app.schemas.auth import AdminSessionUser

_current_admin_audit_context: ContextVar[dict[str, str] | None] = ContextVar(
    "current_admin_audit_context",
    default=None,
)

_FALLBACK_AUDIT_EVENTS: list[AdminActivityRecord] = []


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_current_admin_audit_context(user: AdminSessionUser, *, route_path: str | None = None) -> None:
    _current_admin_audit_context.set(
        {
            "username": user.username,
            "display_name": user.display_name,
            "role": user.role,
            "route_path": route_path or "",
        }
    )


def get_current_admin_audit_context() -> dict[str, str]:
    return dict(_current_admin_audit_context.get() or {})


def _activity_from_orm(row: AdminAuditEventORM) -> AdminActivityRecord:
    actor_label = row.actor_display_name or row.actor_username
    detail = row.detail
    if actor_label:
        detail = f"{detail} Actor: {actor_label}."

    return AdminActivityRecord(
        activity_id=row.audit_id,
        kind=row.kind,
        title=row.title,
        detail=detail,
        status=row.status,
        citation_label=row.citation_label,
        record_id=row.record_id,
        created_at=row.created_at.replace(tzinfo=timezone.utc).isoformat() if row.created_at.tzinfo is None else row.created_at.isoformat(),
    )


def write_admin_audit_event(
    *,
    kind: str,
    title: str,
    detail: str,
    status: str,
    citation_label: str | None = None,
    record_id: str | None = None,
    metadata: dict[str, object] | None = None,
    actor: AdminSessionUser | None = None,
    route_path: str | None = None,
) -> AdminActivityRecord:
    context = _current_admin_audit_context.get() or {}
    actor_username = actor.username if actor else context.get("username")
    actor_display_name = actor.display_name if actor else context.get("display_name")
    actor_role = actor.role if actor else context.get("role")
    resolved_route_path = route_path or context.get("route_path")
    audit_id = str(uuid4())
    created_at = datetime.now(timezone.utc)

    activity = AdminActivityRecord(
        activity_id=audit_id,
        kind=kind,
        title=title,
        detail=f"{detail} Actor: {actor_display_name or actor_username or 'unknown'}." if (actor_display_name or actor_username) else detail,
        status=status,
        citation_label=citation_label,
        record_id=record_id,
        created_at=created_at.isoformat(),
    )

    status_snapshot = get_database_status()
    session_factory = get_session_factory()
    if not status_snapshot["ready"] or session_factory is None:
        _FALLBACK_AUDIT_EVENTS.insert(0, activity)
        del _FALLBACK_AUDIT_EVENTS[100:]
        return activity

    try:
        with session_factory() as session:
            session.add(
                AdminAuditEventORM(
                    audit_id=audit_id,
                    actor_username=actor_username,
                    actor_display_name=actor_display_name,
                    actor_role=actor_role,
                    kind=kind,
                    title=title,
                    detail=detail,
                    status=status,
                    citation_label=citation_label,
                    record_id=record_id,
                    route_path=resolved_route_path,
                    event_metadata=dict(metadata or {}),
                    created_at=created_at.replace(tzinfo=None),
                )
            )
            session.commit()
    except SQLAlchemyError:
        _FALLBACK_AUDIT_EVENTS.insert(0, activity)
        del _FALLBACK_AUDIT_EVENTS[100:]

    return activity


def list_admin_audit_events(limit: int = 50) -> list[AdminActivityRecord]:
    status_snapshot = get_database_status()
    session_factory = get_session_factory()
    if not status_snapshot["ready"] or session_factory is None:
        return list(_FALLBACK_AUDIT_EVENTS[:limit])

    try:
        with session_factory() as session:
            rows = session.scalars(
                select(AdminAuditEventORM).order_by(desc(AdminAuditEventORM.created_at)).limit(limit)
            ).all()
        return [_activity_from_orm(row) for row in rows]
    except SQLAlchemyError:
        return list(_FALLBACK_AUDIT_EVENTS[:limit])


def count_admin_audit_events(*, kind: str | None = None) -> int:
    status_snapshot = get_database_status()
    session_factory = get_session_factory()
    if not status_snapshot["ready"] or session_factory is None:
        if kind is None:
            return len(_FALLBACK_AUDIT_EVENTS)
        return sum(1 for item in _FALLBACK_AUDIT_EVENTS if item.kind == kind)

    try:
        with session_factory() as session:
            statement = select(func.count()).select_from(AdminAuditEventORM)
            if kind is not None:
                statement = statement.where(AdminAuditEventORM.kind == kind)
            return int(session.scalar(statement) or 0)
    except SQLAlchemyError:
        if kind is None:
            return len(_FALLBACK_AUDIT_EVENTS)
        return sum(1 for item in _FALLBACK_AUDIT_EVENTS if item.kind == kind)
