from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.db.models import IngestionRunORM, LegalInstrumentORM, LegalInstrumentVersionORM, LegalProvisionORM
from app.db.session import get_database_status, get_session_factory
from app.schemas.legal_corpus import (
    IngestionRunRecord,
    LegalCorpusStorageSnapshot,
    LegalInstrumentRecord,
    LegalInstrumentVersionRecord,
    LegalProvisionRecord,
    NormalizedInstrumentBundle,
)


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def get_legal_corpus_storage_snapshot() -> LegalCorpusStorageSnapshot:
    status = get_database_status()
    session_factory = get_session_factory()
    tables = [
        LegalInstrumentORM.__tablename__,
        LegalInstrumentVersionORM.__tablename__,
        LegalProvisionORM.__tablename__,
        IngestionRunORM.__tablename__,
    ]

    if not status["ready"] or session_factory is None:
        return LegalCorpusStorageSnapshot(
            persistence_mode="in_memory_scaffold" if not status["configured"] else "database_unavailable",
            database_ready=bool(status["ready"]),
            tables=tables,
        )

    try:
        with session_factory() as session:
            return LegalCorpusStorageSnapshot(
                persistence_mode="database",
                database_ready=True,
                instruments=int(session.scalar(select(func.count()).select_from(LegalInstrumentORM)) or 0),
                versions=int(session.scalar(select(func.count()).select_from(LegalInstrumentVersionORM)) or 0),
                provisions=int(session.scalar(select(func.count()).select_from(LegalProvisionORM)) or 0),
                ingestion_runs=int(session.scalar(select(func.count()).select_from(IngestionRunORM)) or 0),
                tables=tables,
            )
    except SQLAlchemyError:
        return LegalCorpusStorageSnapshot(
            persistence_mode="database_error",
            database_ready=False,
            tables=tables,
        )


def upsert_instrument_bundle(bundle: NormalizedInstrumentBundle) -> bool:
    session_factory = get_session_factory()
    if session_factory is None:
        return False

    with session_factory() as session:
        instrument = session.get(LegalInstrumentORM, bundle.instrument.instrument_id) or LegalInstrumentORM(
            instrument_id=bundle.instrument.instrument_id
        )
        instrument.title = bundle.instrument.title
        instrument.short_title = bundle.instrument.short_title
        instrument.jurisdiction = bundle.instrument.jurisdiction
        instrument.government_level = bundle.instrument.government_level
        instrument.province = bundle.instrument.province
        instrument.category = bundle.instrument.category
        instrument.law_type = bundle.instrument.law_type
        instrument.promulgation_date = _parse_date(bundle.instrument.promulgation_date)
        instrument.effective_date = _parse_date(bundle.instrument.effective_date)
        instrument.status = bundle.instrument.status
        instrument.official_citation = bundle.instrument.official_citation
        instrument.source_url = bundle.instrument.source_url
        instrument.gazette_reference = bundle.instrument.gazette_reference
        instrument.language = bundle.instrument.language
        instrument.current_version_id = bundle.instrument.current_version_id
        instrument.amendment_notes = bundle.instrument.amendment_notes
        instrument.admin_review_status = bundle.instrument.admin_review_status
        instrument.provenance_source_slug = bundle.instrument.provenance_source_slug
        session.merge(instrument)

        version = session.get(LegalInstrumentVersionORM, bundle.version.version_id) or LegalInstrumentVersionORM(
            version_id=bundle.version.version_id
        )
        version.instrument_id = bundle.version.instrument_id
        version.source_slug = bundle.version.source_slug
        version.source_url = bundle.version.source_url
        version.source_trust_level = bundle.version.source_trust_level
        version.version_label = bundle.version.version_label
        version.version_date = _parse_date(bundle.version.version_date)
        version.promulgation_date = _parse_date(bundle.version.promulgation_date)
        version.effective_date = _parse_date(bundle.version.effective_date)
        version.publication_status = bundle.version.publication_status
        version.language = bundle.version.language
        version.content_hash = bundle.version.content_hash
        version.source_format = bundle.version.source_format
        version.gazette_reference = bundle.version.gazette_reference
        version.amendment_notes = bundle.version.amendment_notes
        version.raw_text = bundle.version.raw_text
        version.cleaned_text = bundle.version.cleaned_text
        version.admin_review_status = bundle.version.admin_review_status
        version.extraction_metadata = dict(bundle.version.extraction_metadata)
        session.merge(version)

        existing_provisions = session.scalars(
            select(LegalProvisionORM).where(LegalProvisionORM.version_id == bundle.version.version_id)
        ).all()
        existing_ids = {item.provision_id for item in existing_provisions}

        incoming_ids = {provision.provision_id for provision in bundle.provisions}
        for provision in bundle.provisions:
            row = session.get(LegalProvisionORM, provision.provision_id) or LegalProvisionORM(
                provision_id=provision.provision_id
            )
            row.instrument_id = provision.instrument_id
            row.version_id = provision.version_id
            row.provision_path = provision.provision_path
            row.part_number = provision.part_number
            row.chapter_number = provision.chapter_number
            row.section_number = provision.section_number
            row.subsection_number = provision.subsection_number
            row.heading = provision.heading
            row.body_text = provision.body_text
            row.summary = provision.summary
            row.citations = list(provision.citations)
            row.sort_index = provision.sort_index
            row.retrieval_ready = provision.retrieval_ready
            session.merge(row)

        for stale_id in existing_ids - incoming_ids:
            stale = session.get(LegalProvisionORM, stale_id)
            if stale is not None:
                session.delete(stale)

        session.commit()
    return True


def record_ingestion_run(run: IngestionRunRecord) -> bool:
    session_factory = get_session_factory()
    if session_factory is None:
        return False

    with session_factory() as session:
        row = session.get(IngestionRunORM, run.run_id) or IngestionRunORM(run_id=run.run_id)
        row.adapter_key = run.adapter_key
        row.scope_label = run.scope_label
        row.jurisdiction = run.jurisdiction
        row.government_level = run.government_level
        row.status = run.status
        row.discovered_documents = run.discovered_documents
        row.imported_instruments = run.imported_instruments
        row.imported_versions = run.imported_versions
        row.imported_provisions = run.imported_provisions
        row.duplicate_candidates = run.duplicate_candidates
        row.run_metadata = dict(run.run_metadata)
        row.started_at = _parse_datetime(run.started_at)
        row.finished_at = _parse_datetime(run.finished_at)
        session.merge(row)
        session.commit()
    return True


def list_corpus_instruments(limit: int = 50) -> list[LegalInstrumentRecord]:
    session_factory = get_session_factory()
    if session_factory is None:
        return []

    with session_factory() as session:
        rows = (
            session.scalars(select(LegalInstrumentORM).order_by(LegalInstrumentORM.title.asc()).limit(limit)).all()
        )
    return [
        LegalInstrumentRecord(
            instrument_id=row.instrument_id,
            title=row.title,
            short_title=row.short_title,
            jurisdiction=row.jurisdiction,
            government_level=row.government_level,
            province=row.province,
            category=row.category,
            law_type=row.law_type,
            promulgation_date=row.promulgation_date.isoformat() if row.promulgation_date else None,
            effective_date=row.effective_date.isoformat() if row.effective_date else None,
            status=row.status,
            official_citation=row.official_citation,
            source_url=row.source_url,
            gazette_reference=row.gazette_reference,
            language=row.language,
            current_version_id=row.current_version_id,
            amendment_notes=row.amendment_notes,
            admin_review_status=row.admin_review_status,
            provenance_source_slug=row.provenance_source_slug,
        )
        for row in rows
    ]
