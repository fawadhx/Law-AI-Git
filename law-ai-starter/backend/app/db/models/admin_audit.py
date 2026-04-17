from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base


class AdminAuditEventORM(Base):
    __tablename__ = "admin_audit_events"
    __table_args__ = (
        Index("ix_admin_audit_kind_created", "kind", "created_at"),
        Index("ix_admin_audit_actor_created", "actor_username", "created_at"),
        Index("ix_admin_audit_record_created", "record_id", "created_at"),
    )

    audit_id: Mapped[str] = mapped_column(String(120), primary_key=True)
    actor_username: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    actor_display_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    actor_role: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    kind: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    citation_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    record_id: Mapped[str | None] = mapped_column(String(160), nullable=True)
    route_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    event_metadata: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
