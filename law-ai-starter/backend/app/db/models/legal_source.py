from __future__ import annotations

import hashlib

from sqlalchemy import DateTime, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.core.config import settings
from app.db.base import Base
from app.schemas.legal_source import LegalSourceRecord


def _normalize_retrieval_document(value: str) -> str:
    return " ".join(part.strip() for part in value.split() if part.strip())


def _build_retrieval_document(record: LegalSourceRecord) -> str:
    ordered_parts = [
        record.citation_label,
        record.law_name,
        record.section_number,
        record.section_title,
        record.summary,
        record.excerpt,
        " ".join(record.tags),
        " ".join(record.aliases),
        " ".join(record.keywords),
        " ".join(record.related_sections),
        record.offence_group or "",
        record.punishment_summary or "",
        record.provision_kind,
        record.source_title,
    ]
    return _normalize_retrieval_document(" ".join(part for part in ordered_parts if part))


def _build_retrieval_fingerprint(document: str) -> str:
    return hashlib.sha256(document.encode("utf-8")).hexdigest()


class LegalSourceORM(Base):
    __tablename__ = "legal_source_records"
    __table_args__ = (
        Index("ix_legal_source_law_section", "law_name", "section_number"),
        Index("ix_legal_source_kind_group", "provision_kind", "offence_group"),
        Index("ix_legal_source_retrieval_fingerprint", "retrieval_fingerprint"),
        Index("ix_legal_source_embedding_status", "embedding_status"),
    )

    id: Mapped[str] = mapped_column(String(120), primary_key=True)
    source_title: Mapped[str] = mapped_column(String(255), nullable=False)
    law_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    section_number: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    section_title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    citation_label: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    jurisdiction: Mapped[str] = mapped_column(String(120), nullable=False, default="Pakistan")

    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list)
    keywords: Mapped[list[str]] = mapped_column(JSON, default=list)
    related_sections: Mapped[list[str]] = mapped_column(JSON, default=list)
    searchable_terms: Mapped[list[str]] = mapped_column(JSON, default=list)

    offence_group: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    punishment_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    provision_kind: Mapped[str] = mapped_column(String(64), nullable=False, default="general", index=True)
    retrieval_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    retrieval_document: Mapped[str] = mapped_column(Text, nullable=False, default="")
    retrieval_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False, default="", index=True)

    embedding_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending", index=True)
    embedding_model: Mapped[str | None] = mapped_column(String(120), nullable=True)
    embedding_dimensions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    embedding_updated_at: Mapped[object | None] = mapped_column(DateTime(timezone=True), nullable=True)

    source_status: Mapped[str] = mapped_column(String(32), nullable=False, default="published", index=True)

    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    @classmethod
    def from_record(cls, record: LegalSourceRecord) -> "LegalSourceORM":
        retrieval_document = record.retrieval_document or _build_retrieval_document(record)
        retrieval_fingerprint = record.retrieval_fingerprint or _build_retrieval_fingerprint(retrieval_document)
        return cls(
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
            searchable_terms=list(record.searchable_parts),
            offence_group=record.offence_group,
            punishment_summary=record.punishment_summary,
            provision_kind=record.provision_kind,
            retrieval_text="\n".join(part for part in record.searchable_parts if part),
            retrieval_document=retrieval_document,
            retrieval_fingerprint=retrieval_fingerprint,
            embedding_status=record.embedding_status or "pending",
            embedding_model=record.embedding_model or settings.legal_source_embedding_model,
            embedding_dimensions=record.embedding_dimensions or settings.legal_source_embedding_dimensions,
            embedding_updated_at=None,
            source_status="published",
        )

    def to_record(self) -> LegalSourceRecord:
        return LegalSourceRecord(
            id=self.id,
            source_title=self.source_title,
            law_name=self.law_name,
            section_number=self.section_number,
            section_title=self.section_title,
            summary=self.summary,
            excerpt=self.excerpt,
            citation_label=self.citation_label,
            jurisdiction=self.jurisdiction,
            tags=list(self.tags or []),
            aliases=list(self.aliases or []),
            keywords=list(self.keywords or []),
            related_sections=list(self.related_sections or []),
            offence_group=self.offence_group,
            punishment_summary=self.punishment_summary,
            provision_kind=self.provision_kind,
            retrieval_document=self.retrieval_document or self.retrieval_text or "",
            retrieval_fingerprint=self.retrieval_fingerprint or None,
            embedding_status=self.embedding_status or None,
            embedding_model=self.embedding_model or None,
            embedding_dimensions=self.embedding_dimensions,
            embedding_updated_at=self.embedding_updated_at.isoformat() if self.embedding_updated_at else None,
        )
