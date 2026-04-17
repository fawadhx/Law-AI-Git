from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base


class LegalInstrumentORM(Base):
    __tablename__ = "legal_instruments"
    __table_args__ = (
        Index("ix_legal_instrument_title_level", "title", "government_level"),
        Index("ix_legal_instrument_status_review", "status", "admin_review_status"),
    )

    instrument_id: Mapped[str] = mapped_column(String(160), primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    short_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    jurisdiction: Mapped[str] = mapped_column(String(120), nullable=False, default="Pakistan")
    government_level: Mapped[str] = mapped_column(String(32), nullable=False, default="federal", index=True)
    province: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    category: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    law_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    promulgation_date: Mapped[object | None] = mapped_column(Date, nullable=True)
    effective_date: Mapped[object | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="unknown", index=True)
    official_citation: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    gazette_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    language: Mapped[str] = mapped_column(String(16), nullable=False, default="en")
    current_version_id: Mapped[str | None] = mapped_column(String(160), nullable=True)
    amendment_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    admin_review_status: Mapped[str] = mapped_column(String(32), nullable=False, default="imported_unreviewed")
    provenance_source_slug: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    extra_metadata: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class LegalInstrumentVersionORM(Base):
    __tablename__ = "legal_instrument_versions"
    __table_args__ = (
        Index("ix_legal_version_instrument_review", "instrument_id", "admin_review_status"),
        Index("ix_legal_version_source_slug", "source_slug"),
        Index("ix_legal_version_content_hash", "content_hash"),
    )

    version_id: Mapped[str] = mapped_column(String(160), primary_key=True)
    instrument_id: Mapped[str] = mapped_column(
        String(160),
        ForeignKey("legal_instruments.instrument_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_slug: Mapped[str] = mapped_column(String(80), nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    source_trust_level: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    version_label: Mapped[str | None] = mapped_column(String(120), nullable=True)
    version_date: Mapped[object | None] = mapped_column(Date, nullable=True)
    promulgation_date: Mapped[object | None] = mapped_column(Date, nullable=True)
    effective_date: Mapped[object | None] = mapped_column(Date, nullable=True)
    publication_status: Mapped[str] = mapped_column(String(32), nullable=False, default="unknown", index=True)
    language: Mapped[str] = mapped_column(String(16), nullable=False, default="en")
    content_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    source_format: Mapped[str] = mapped_column(String(32), nullable=False, default="html")
    gazette_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    amendment_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    cleaned_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    admin_review_status: Mapped[str] = mapped_column(String(32), nullable=False, default="imported_unreviewed")
    extraction_metadata: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class LegalProvisionORM(Base):
    __tablename__ = "legal_provisions"
    __table_args__ = (
        Index("ix_legal_provision_instrument_version", "instrument_id", "version_id"),
        Index("ix_legal_provision_section_path", "section_number", "provision_path"),
        Index("ix_legal_provision_retrieval_ready", "retrieval_ready"),
    )

    provision_id: Mapped[str] = mapped_column(String(200), primary_key=True)
    instrument_id: Mapped[str] = mapped_column(
        String(160),
        ForeignKey("legal_instruments.instrument_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version_id: Mapped[str] = mapped_column(
        String(160),
        ForeignKey("legal_instrument_versions.version_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    section_type: Mapped[str] = mapped_column(String(64), nullable=False, default="section")
    provision_path: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_section_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    part_number: Mapped[str | None] = mapped_column(String(64), nullable=True)
    chapter_number: Mapped[str | None] = mapped_column(String(64), nullable=True)
    section_number: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    subsection_number: Mapped[str | None] = mapped_column(String(64), nullable=True)
    heading: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body_text: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    citations: Mapped[list[str]] = mapped_column(JSON, default=list)
    sort_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    retrieval_ready: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class IngestionRunORM(Base):
    __tablename__ = "ingestion_runs"
    __table_args__ = (
        Index("ix_ingestion_run_adapter_status", "adapter_key", "status"),
        Index("ix_ingestion_run_scope_level", "scope_label", "government_level"),
    )

    run_id: Mapped[str] = mapped_column(String(120), primary_key=True)
    adapter_key: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    scope_label: Mapped[str] = mapped_column(String(160), nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String(120), nullable=False, default="Pakistan")
    government_level: Mapped[str] = mapped_column(String(32), nullable=False, default="federal")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="planned")
    discovered_documents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    imported_instruments: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    imported_versions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    imported_provisions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    duplicate_candidates: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    run_metadata: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
