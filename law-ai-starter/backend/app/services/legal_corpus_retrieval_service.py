from __future__ import annotations

import hashlib

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.db.models import LegalInstrumentORM, LegalInstrumentVersionORM, LegalProvisionORM
from app.db.session import get_session_factory
from app.schemas.legal_source import LegalSourceRecord


REVIEW_READY_STATUSES = {"reviewed", "approved", "published", "retrieval_ready"}


def _normalize_text(value: str) -> str:
    return " ".join(part.strip() for part in value.split() if part.strip())


def _shorten_text(value: str, *, limit: int) -> str:
    cleaned = _normalize_text(value)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def _derive_law_name(instrument: LegalInstrumentORM) -> str:
    return instrument.short_title or instrument.title


def _derive_section_title(provision: LegalProvisionORM) -> str:
    return provision.heading or provision.provision_path or "Structured section"


def _derive_section_number(provision: LegalProvisionORM) -> str:
    return provision.section_number or provision.provision_path or provision.provision_id


def _derive_summary(provision: LegalProvisionORM) -> str:
    if provision.summary:
        return _shorten_text(provision.summary, limit=280)
    return _shorten_text(provision.body_text, limit=280)


def _derive_excerpt(provision: LegalProvisionORM) -> str:
    return _shorten_text(provision.body_text, limit=700)


def _derive_provision_kind(provision: LegalProvisionORM) -> str:
    heading = (provision.heading or "").lower()
    path = (provision.provision_path or "").lower()
    summary = (provision.summary or "").lower()
    body = (provision.body_text or "").lower()
    haystack = " ".join([heading, path, summary, body])

    if "punishment" in haystack:
        return "punishment"
    if any(keyword in haystack for keyword in ["means", "definition", "is said to", "shall mean"]):
        return "definition"
    if provision.section_type == "subsection":
        return "subsection"
    return "general"


def _build_provenance(instrument: LegalInstrumentORM, version: LegalInstrumentVersionORM) -> str:
    authority = (version.extraction_metadata or {}).get("source_authority") or (instrument.extra_metadata or {}).get(
        "source_authority"
    )
    trust_level = version.source_trust_level
    parts = [str(authority).strip()] if authority else []
    if trust_level:
        parts.append(f"trust: {trust_level}")
    if version.source_url:
        parts.append("official source")
    return " | ".join(part for part in parts if part)


def _build_citation_label(law_name: str, provision: LegalProvisionORM) -> str:
    section_number = _derive_section_number(provision)
    return f"{law_name} Section {section_number}"


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
        record.summary,
        record.excerpt,
        " ".join(record.tags),
        " ".join(record.aliases),
        " ".join(record.keywords),
        " ".join(record.related_sections),
        record.offence_group or "",
        record.punishment_summary or "",
        record.provision_kind,
        record.provenance or "",
        record.source_url or "",
    ]
    return _normalize_text(" ".join(part for part in ordered_parts if part))


def _build_retrieval_fingerprint(document: str) -> str:
    return hashlib.sha256(document.encode("utf-8")).hexdigest()


def _map_provision_to_legal_source_record(
    instrument: LegalInstrumentORM,
    version: LegalInstrumentVersionORM,
    provision: LegalProvisionORM,
) -> LegalSourceRecord:
    law_name = _derive_law_name(instrument)
    section_number = _derive_section_number(provision)
    section_title = _derive_section_title(provision)
    summary = _derive_summary(provision)
    excerpt = _derive_excerpt(provision)
    provision_kind = _derive_provision_kind(provision)
    provenance = _build_provenance(instrument, version)

    tags = [
        instrument.category,
        instrument.law_type,
        provision.section_type,
        f"{instrument.government_level} law",
    ]
    if instrument.province:
        tags.append(instrument.province)

    keywords = [section_number, section_title]
    if instrument.official_citation:
        keywords.append(instrument.official_citation)
    if instrument.gazette_reference:
        keywords.append(instrument.gazette_reference)

    record = LegalSourceRecord(
        id=provision.provision_id,
        source_title=instrument.title,
        law_name=law_name,
        section_number=section_number,
        section_title=section_title,
        summary=summary,
        excerpt=excerpt,
        citation_label=_build_citation_label(law_name, provision),
        country=instrument.jurisdiction,
        jurisdiction=instrument.jurisdiction,
        jurisdiction_type=instrument.government_level,
        government_level=instrument.government_level,
        province=instrument.province,
        law_category=instrument.category,
        law_type=instrument.law_type,
        source_status=version.publication_status,
        official_citation=instrument.official_citation,
        enactment_year=instrument.promulgation_date.year if instrument.promulgation_date else None,
        effective_year=instrument.effective_date.year if instrument.effective_date else None,
        tags=[tag for tag in tags if tag],
        aliases=[instrument.short_title] if instrument.short_title else [],
        keywords=[value for value in keywords if value],
        related_sections=list(provision.citations or []),
        punishment_summary=summary if provision_kind == "punishment" else None,
        provision_kind=provision_kind,
        source_url=version.source_url,
        source_last_verified=None,
        amendment_notes=version.amendment_notes or instrument.amendment_notes,
        provenance=provenance or None,
        source_trust_level=version.source_trust_level,
        retrieval_source_type="legal_corpus",
    )
    retrieval_document = _build_retrieval_document(record)
    return record.model_copy(
        update={
            "retrieval_document": retrieval_document,
            "retrieval_fingerprint": _build_retrieval_fingerprint(retrieval_document),
        }
    )


def list_retrieval_ready_legal_corpus_records() -> list[LegalSourceRecord]:
    session_factory = get_session_factory()
    if session_factory is None:
        return []

    try:
        with session_factory() as session:
            rows = session.execute(
                select(LegalProvisionORM, LegalInstrumentORM, LegalInstrumentVersionORM)
                .join(LegalInstrumentORM, LegalInstrumentORM.instrument_id == LegalProvisionORM.instrument_id)
                .join(LegalInstrumentVersionORM, LegalInstrumentVersionORM.version_id == LegalProvisionORM.version_id)
                .where(LegalProvisionORM.retrieval_ready.is_(True))
                .where(LegalInstrumentORM.admin_review_status.in_(REVIEW_READY_STATUSES))
                .where(LegalInstrumentVersionORM.admin_review_status.in_(REVIEW_READY_STATUSES))
                .order_by(
                    LegalInstrumentORM.title.asc(),
                    LegalProvisionORM.sort_index.asc(),
                    LegalProvisionORM.provision_id.asc(),
                )
            ).all()
    except SQLAlchemyError:
        return []

    return [_map_provision_to_legal_source_record(instrument, version, provision) for provision, instrument, version in rows]


def get_legal_corpus_retrieval_snapshot() -> dict[str, object]:
    records = list_retrieval_ready_legal_corpus_records()
    return {
        "record_count": len(records),
        "indexed_record_count": len(records),
        "vector_prepared_count": len(records),
        "retrieval_mode": "structured_sections_keyword_ready",
        "records": records,
    }
