from __future__ import annotations

import hashlib
import re

from app.schemas.legal_corpus import (
    LegalInstrumentRecord,
    LegalInstrumentVersionRecord,
    LegalStructuredSectionRecord,
    NormalizedInstrumentBundle,
    RawSourceDocumentInput,
)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "item"


def _build_instrument_id(payload: RawSourceDocumentInput) -> str:
    level = payload.government_level.lower()
    province = f"-{_slugify(payload.province)}" if payload.province else ""
    return f"pk-{level}{province}-{_slugify(payload.title)}"


def _build_version_id(payload: RawSourceDocumentInput, instrument_id: str) -> str:
    suffix_seed = "|".join(
        [
            payload.source_slug,
            payload.version_label or "",
            payload.version_date or "",
            payload.gazette_reference or "",
            payload.source_url,
        ]
    )
    fingerprint = hashlib.sha256(suffix_seed.encode("utf-8")).hexdigest()[:12]
    return f"{instrument_id}-v-{fingerprint}"


def _normalize_cleaned_text(payload: RawSourceDocumentInput) -> str | None:
    candidate = payload.cleaned_text or payload.raw_text
    if not candidate:
        return None
    return "\n".join(line.rstrip() for line in candidate.splitlines()).strip()


def normalize_source_document(payload: RawSourceDocumentInput) -> NormalizedInstrumentBundle:
    instrument_id = _build_instrument_id(payload)
    version_id = _build_version_id(payload, instrument_id)
    cleaned_text = _normalize_cleaned_text(payload)
    raw_text = payload.raw_text.strip() if payload.raw_text else None
    content_hash = None
    if cleaned_text:
        content_hash = hashlib.sha256(cleaned_text.encode("utf-8")).hexdigest()

    instrument = LegalInstrumentRecord(
        instrument_id=instrument_id,
        title=payload.title,
        short_title=payload.short_title,
        jurisdiction=payload.jurisdiction,
        government_level=payload.government_level,
        province=payload.province,
        category=payload.category,
        law_type=payload.law_type,
        promulgation_date=payload.promulgation_date,
        effective_date=payload.effective_date,
        status=payload.status,
        official_citation=payload.official_citation,
        source_url=payload.source_url,
        gazette_reference=payload.gazette_reference,
        language=payload.language,
        current_version_id=version_id,
        amendment_notes=payload.amendment_notes,
        admin_review_status="imported_unreviewed",
        provenance_source_slug=payload.source_slug,
        source_authority=payload.source_authority,
    )
    version = LegalInstrumentVersionRecord(
        version_id=version_id,
        instrument_id=instrument_id,
        source_slug=payload.source_slug,
        source_url=payload.source_url,
        source_trust_level=payload.source_trust_level,
        version_label=payload.version_label,
        version_date=payload.version_date,
        promulgation_date=payload.promulgation_date,
        effective_date=payload.effective_date,
        publication_status=payload.status,
        language=payload.language,
        content_hash=content_hash,
        source_format=payload.source_format,
        gazette_reference=payload.gazette_reference,
        amendment_notes=payload.amendment_notes,
        raw_text=raw_text,
        cleaned_text=cleaned_text,
        admin_review_status="imported_unreviewed",
        extraction_metadata=dict(payload.extraction_metadata),
        source_authority=payload.source_authority,
    )
    return NormalizedInstrumentBundle(
        instrument=instrument,
        version=version,
        structured_sections=[],
    )


def make_provision_record(
    *,
    instrument_id: str,
    version_id: str,
    provision_path: str,
    body_text: str,
    sort_index: int,
    heading: str | None = None,
    part_number: str | None = None,
    chapter_number: str | None = None,
    section_number: str | None = None,
    subsection_number: str | None = None,
    summary: str | None = None,
    citations: list[str] | None = None,
) -> LegalStructuredSectionRecord:
    section_id = f"{version_id}-{_slugify(provision_path)}"
    return LegalStructuredSectionRecord(
        section_id=section_id,
        instrument_id=instrument_id,
        version_id=version_id,
        section_type="section" if subsection_number is None else "subsection",
        section_path=provision_path,
        parent_section_path=section_number if subsection_number else None,
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
