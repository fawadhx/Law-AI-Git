from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base


class LegalSourceVersionORM(Base):
    __tablename__ = "legal_source_versions"
    __table_args__ = (
        Index("ix_legal_source_version_record_created", "record_id", "created_at"),
        Index("ix_legal_source_version_record_number", "record_id", "version_number"),
        Index("ix_legal_source_version_action_created", "action", "created_at"),
    )

    version_id: Mapped[str] = mapped_column(String(120), primary_key=True)
    record_id: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    citation_label: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    changed_fields: Mapped[list[dict[str, object]]] = mapped_column(JSON, default=list)
    snapshot: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    actor_username: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    actor_role: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    audit_id: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
