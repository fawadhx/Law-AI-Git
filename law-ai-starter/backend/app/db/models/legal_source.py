from sqlalchemy import Index, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.base import Base
from app.schemas.legal_source import LegalSourceRecord


class LegalSourceORM(Base):
    __tablename__ = "legal_source_records"
    __table_args__ = (
        Index("ix_legal_source_law_section", "law_name", "section_number"),
        Index("ix_legal_source_kind_group", "provision_kind", "offence_group"),
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
        )
