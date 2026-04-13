from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.data.legal_sources import LEGAL_SOURCES
from app.db.bootstrap import get_database_foundation_snapshot
from app.db.models import LegalSourceORM
from app.db.session import get_session_factory
from app.schemas.legal_source import LegalSourceRecord


@dataclass(slots=True)
class LegalSourceStoreSnapshot:
    active_source: str
    source_label: str
    database_ready: bool
    foundation_stage: str
    active_record_count: int
    persisted_record_count: int
    detail: str
    records: list[LegalSourceRecord] = field(default_factory=list)


@dataclass(slots=True)
class LegalSourceStoreStatus:
    active_source: str
    source_label: str
    database_ready: bool
    foundation_stage: str
    active_record_count: int
    persisted_record_count: int
    detail: str


def _section_sort_key(value: str) -> tuple[int, str]:
    digits = "".join(character for character in value if character.isdigit())
    if digits:
        return (0, digits.zfill(6))
    return (1, value.lower())


def _sort_records(records: list[LegalSourceRecord]) -> list[LegalSourceRecord]:
    return sorted(
        records,
        key=lambda record: (
            record.law_name.lower(),
            _section_sort_key(record.section_number),
            record.section_title.lower(),
            record.id.lower(),
        ),
    )


def _build_status(snapshot: LegalSourceStoreSnapshot) -> LegalSourceStoreStatus:
    return LegalSourceStoreStatus(
        active_source=snapshot.active_source,
        source_label=snapshot.source_label,
        database_ready=snapshot.database_ready,
        foundation_stage=snapshot.foundation_stage,
        active_record_count=snapshot.active_record_count,
        persisted_record_count=snapshot.persisted_record_count,
        detail=snapshot.detail,
    )


def _normalize_retrieval_document(value: str) -> str:
    return " ".join(part.strip() for part in value.split() if part.strip())


def build_retrieval_document(record: LegalSourceRecord) -> str:
    if record.retrieval_document:
        return _normalize_retrieval_document(record.retrieval_document)

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


def build_retrieval_fingerprint(record: LegalSourceRecord) -> str:
    if record.retrieval_fingerprint:
        return record.retrieval_fingerprint
    return hashlib.sha256(build_retrieval_document(record).encode("utf-8")).hexdigest()


def get_record_searchable_text(record: LegalSourceRecord) -> str:
    return build_retrieval_document(record) or _normalize_retrieval_document(" ".join(record.searchable_parts))


def _vector_readiness_label(*, vector_stage: str, coverage_percent: int) -> str:
    if vector_stage == "vector_not_configured":
        return "Vector layer not configured"
    if vector_stage == "vector_database_unavailable":
        return "Database not ready for retrieval metadata"
    if vector_stage == "vector_database_ready_empty":
        return "Database ready but empty"
    if vector_stage == "embedding_metadata_pending":
        return f"Embedding metadata pending ({coverage_percent}% ready)"
    if vector_stage == "embedding_metadata_ready":
        return "Embedding metadata foundation ready"
    if vector_stage == "vector_search_flag_enabled":
        return "Vector-search flag enabled"
    return "Vector readiness unknown"


def get_legal_source_store_diagnostics(*, prefer_database: bool = True) -> dict[str, object]:
    snapshot = get_legal_source_store_snapshot(prefer_database=prefer_database)
    foundation = get_database_foundation_snapshot()

    embedding_ready_records = int(foundation.get("embedding_ready_records", 0) or 0)
    embedding_pending_records = int(foundation.get("embedding_pending_records", 0) or 0)
    embedding_coverage_percent = int(foundation.get("embedding_coverage_percent", 0) or 0)
    vector_stage = str(foundation.get("vector_stage", "vector_not_configured"))

    retrieval_profile = (
        "normalized_database_documents"
        if snapshot.active_source == "database"
        else "in_memory_searchable_parts"
    )
    retrieval_profile_label = (
        "Normalized database retrieval documents"
        if snapshot.active_source == "database"
        else "In-memory searchable parts"
    )

    return {
        "active_source": snapshot.active_source,
        "source_label": snapshot.source_label,
        "database_ready": snapshot.database_ready,
        "foundation_stage": snapshot.foundation_stage,
        "active_record_count": snapshot.active_record_count,
        "persisted_record_count": snapshot.persisted_record_count,
        "detail": snapshot.detail,
        "retrieval_profile": retrieval_profile,
        "retrieval_profile_label": retrieval_profile_label,
        "embedding_ready_records": embedding_ready_records,
        "embedding_pending_records": embedding_pending_records,
        "embedding_coverage_percent": embedding_coverage_percent,
        "vector_stage": vector_stage,
        "vector_readiness_label": _vector_readiness_label(
            vector_stage=vector_stage,
            coverage_percent=embedding_coverage_percent,
        ),
        "embedding_model": settings.legal_source_embedding_model,
        "embedding_dimensions": settings.legal_source_embedding_dimensions,
        "vector_search_enabled": settings.legal_source_vector_search_enabled,
    }


def _in_memory_snapshot(*, detail: str, persisted_record_count: int, database_ready: bool, foundation_stage: str) -> LegalSourceStoreSnapshot:
    records = _sort_records(list(LEGAL_SOURCES))
    return LegalSourceStoreSnapshot(
        active_source="in_memory",
        source_label="In-memory prototype catalog",
        database_ready=database_ready,
        foundation_stage=foundation_stage,
        active_record_count=len(records),
        persisted_record_count=persisted_record_count,
        detail=detail,
        records=records,
    )


def get_legal_source_store_snapshot(*, prefer_database: bool = True) -> LegalSourceStoreSnapshot:
    foundation = get_database_foundation_snapshot()
    persisted_record_count = int(foundation.get("persisted_records", 0) or 0)
    database_ready = bool(foundation.get("ready"))
    foundation_stage = str(foundation.get("foundation_stage", "in_memory_only"))
    detail = str(foundation.get("detail") or "")
    embedding_coverage = int(foundation.get("embedding_coverage_percent", 0) or 0)
    vector_stage = str(foundation.get("vector_stage", "vector_not_configured"))

    if not prefer_database or not database_ready:
        fallback_detail = (
            "The active legal source store is currently the in-memory prototype catalog. "
            + detail
            + " "
            + _vector_readiness_label(vector_stage=vector_stage, coverage_percent=embedding_coverage)
        ).strip()
        return _in_memory_snapshot(
            detail=fallback_detail,
            persisted_record_count=persisted_record_count,
            database_ready=database_ready,
            foundation_stage=foundation_stage,
        )

    session_factory = get_session_factory()
    if session_factory is None:
        return _in_memory_snapshot(
            detail="Database is configured, but no session factory is available yet, so the active legal source store remains the in-memory prototype catalog.",
            persisted_record_count=persisted_record_count,
            database_ready=False,
            foundation_stage="database_not_ready",
        )

    try:
        with session_factory() as session:
            rows = session.scalars(select(LegalSourceORM)).all()
        if rows:
            records = _sort_records([row.to_record() for row in rows])
            return LegalSourceStoreSnapshot(
                active_source="database",
                source_label="Persisted database catalog",
                database_ready=True,
                foundation_stage=foundation_stage,
                active_record_count=len(records),
                persisted_record_count=persisted_record_count,
                detail=(
                    "The active legal source store is reading from persisted database records with normalized retrieval documents. "
                    + _vector_readiness_label(vector_stage=vector_stage, coverage_percent=embedding_coverage)
                    + (f" {detail}" if detail else "")
                ).strip(),
                records=records,
            )

        return _in_memory_snapshot(
            detail=(
                "Database is ready, but the persisted catalog is empty, so the active legal source store is falling back to the in-memory prototype catalog. "
                + _vector_readiness_label(vector_stage=vector_stage, coverage_percent=embedding_coverage)
                + (f" {detail}" if detail else "")
            ).strip(),
            persisted_record_count=persisted_record_count,
            database_ready=True,
            foundation_stage=foundation_stage,
        )
    except SQLAlchemyError as exc:  # pragma: no cover - depends on environment
        return _in_memory_snapshot(
            detail=f"Database-backed source reading failed ({exc}), so the active legal source store is using the in-memory prototype catalog.",
            persisted_record_count=persisted_record_count,
            database_ready=False,
            foundation_stage="database_error",
        )


def get_legal_source_store_status(*, prefer_database: bool = True) -> LegalSourceStoreStatus:
    return _build_status(get_legal_source_store_snapshot(prefer_database=prefer_database))


def get_active_legal_source_records(*, prefer_database: bool = True) -> list[LegalSourceRecord]:
    return get_legal_source_store_snapshot(prefer_database=prefer_database).records


def get_active_legal_source_record_map(*, prefer_database: bool = True) -> dict[str, LegalSourceRecord]:
    return {record.id: record for record in get_active_legal_source_records(prefer_database=prefer_database)}


def find_active_legal_source_record(record_id: str, *, prefer_database: bool = True) -> LegalSourceRecord | None:
    return get_active_legal_source_record_map(prefer_database=prefer_database).get(record_id)


def upsert_persisted_legal_source(record: LegalSourceRecord) -> bool:
    foundation = get_database_foundation_snapshot()
    session_factory = get_session_factory()
    if not foundation.get("ready") or session_factory is None:
        return False

    try:
        with session_factory() as session:
            session.merge(LegalSourceORM.from_record(record))
            session.commit()
        return True
    except SQLAlchemyError:  # pragma: no cover - depends on environment
        return False
