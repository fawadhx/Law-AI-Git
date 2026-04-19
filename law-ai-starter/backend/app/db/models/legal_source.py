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
        record.country,
        record.law_name,
        record.official_citation or "",
        record.section_number,
        record.section_title,
        record.jurisdiction_type,
        record.law_type or "",
        record.government_level,
        record.province or "",
        record.law_category or "",
        record.source_status or "",
        str(record.enactment_year or ""),
        str(record.effective_year or ""),
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
        record.amendment_notes or "",
        record.source_url or "",
        record.source_last_verified or "",
        record.provenance or "",
        record.source_trust_level or "",
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
    country: Mapped[str] = mapped_column(String(120), nullable=False, default="Pakistan")
    jurisdiction: Mapped[str] = mapped_column(String(120), nullable=False, default="Pakistan")
    jurisdiction_type: Mapped[str] = mapped_column(String(32), nullable=False, default="federal", index=True)
    government_level: Mapped[str] = mapped_column(String(32), nullable=False, default="federal", index=True)
    province: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    law_category: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    law_type: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    source_status: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    official_citation: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    enactment_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    effective_year: Mapped[int | None] = mapped_column(Integer, nullable=True)

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

    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_last_verified: Mapped[str | None] = mapped_column(String(32), nullable=True)
    amendment_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    provenance: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_trust_level: Mapped[str | None] = mapped_column(String(48), nullable=True)
    retrieval_source_type: Mapped[str] = mapped_column(String(48), nullable=False, default="legacy_catalog")

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
            country=record.country,
            jurisdiction=record.jurisdiction,
            jurisdiction_type=record.jurisdiction_type,
            government_level=record.government_level,
            province=record.province,
            law_category=record.law_category,
            law_type=record.law_type,
            source_status=record.source_status or "published",
            official_citation=record.official_citation,
            enactment_year=record.enactment_year,
            effective_year=record.effective_year,
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
            source_url=record.source_url,
            source_last_verified=record.source_last_verified,
            amendment_notes=record.amendment_notes,
            provenance=record.provenance,
            source_trust_level=record.source_trust_level,
            retrieval_source_type=record.retrieval_source_type,
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
            country=self.country or "Pakistan",
            jurisdiction=self.jurisdiction,
            jurisdiction_type=self.jurisdiction_type or self.government_level or "federal",
            government_level=self.government_level or "federal",
            province=self.province,
            law_category=self.law_category,
            law_type=self.law_type,
            source_status=self.source_status,
            official_citation=self.official_citation,
            enactment_year=self.enactment_year,
            effective_year=self.effective_year,
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
            source_url=self.source_url,
            source_last_verified=self.source_last_verified,
            amendment_notes=self.amendment_notes,
            provenance=self.provenance,
            source_trust_level=self.source_trust_level,
            retrieval_source_type=self.retrieval_source_type or "legacy_catalog",
        )
