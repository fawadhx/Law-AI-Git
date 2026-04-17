from __future__ import annotations

from app.schemas.legal_corpus import LegalStructuredSectionRecord


def make_structured_section(
    *,
    section_id: str,
    instrument_id: str,
    version_id: str,
    section_path: str,
    body_text: str,
    sort_index: int,
    section_type: str = "section",
    parent_section_path: str | None = None,
    heading: str | None = None,
    part_number: str | None = None,
    chapter_number: str | None = None,
    section_number: str | None = None,
    subsection_number: str | None = None,
    summary: str | None = None,
    citations: list[str] | None = None,
) -> LegalStructuredSectionRecord:
    return LegalStructuredSectionRecord(
        section_id=section_id,
        instrument_id=instrument_id,
        version_id=version_id,
        section_type=section_type,
        section_path=section_path,
        parent_section_path=parent_section_path,
        part_number=part_number,
        chapter_number=chapter_number,
        section_number=section_number,
        subsection_number=subsection_number,
        heading=heading,
        body_text=body_text.strip(),
        summary=summary,
        citations=list(citations or []),
        sort_index=sort_index,
        retrieval_ready=False,
    )
