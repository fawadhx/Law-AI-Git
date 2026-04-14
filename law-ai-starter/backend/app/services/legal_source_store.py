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


def build_canonical_retrieval_document(record: LegalSourceRecord) -> str:
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


def build_retrieval_document(record: LegalSourceRecord) -> str:
    if record.retrieval_document:
        return _normalize_retrieval_document(record.retrieval_document)
    return build_canonical_retrieval_document(record)


def build_retrieval_fingerprint_for_document(document: str) -> str:
    return hashlib.sha256(document.encode("utf-8")).hexdigest()


def build_retrieval_fingerprint(record: LegalSourceRecord) -> str:
    if record.retrieval_fingerprint:
        return record.retrieval_fingerprint
    return build_retrieval_fingerprint_for_document(build_retrieval_document(record))


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


def _build_canonical_record(record: LegalSourceRecord) -> LegalSourceRecord:
    return record.model_copy(update={"retrieval_document": None, "retrieval_fingerprint": None})


def get_persisted_retrieval_readiness_audit(*, limit: int = 12) -> dict[str, object]:
    foundation = get_database_foundation_snapshot()
    session_factory = get_session_factory()
    snapshot = get_legal_source_store_snapshot()

    empty = {
        "active_source": snapshot.active_source,
        "source_label": snapshot.source_label,
        "database_ready": bool(foundation.get("ready")),
        "foundation_stage": str(foundation.get("foundation_stage", "in_memory_only")),
        "persisted_record_count": int(foundation.get("persisted_records", 0) or 0),
        "active_record_count": snapshot.active_record_count,
        "embedding_ready_count": int(foundation.get("embedding_ready_records", 0) or 0),
        "embedding_pending_count": int(foundation.get("embedding_pending_records", 0) or 0),
        "stale_count": 0,
        "missing_document_count": 0,
        "missing_fingerprint_count": 0,
        "refresh_needed_count": 0,
        "vector_candidate_count": 0,
        "sample_records": [],
    }

    if not foundation.get("ready") or session_factory is None:
        return empty

    try:
        with session_factory() as session:
            rows = session.scalars(select(LegalSourceORM)).all()
    except SQLAlchemyError:  # pragma: no cover - depends on environment
        return empty

    sample_records: list[dict[str, object]] = []
    stale_count = 0
    missing_document_count = 0
    missing_fingerprint_count = 0
    refresh_needed_count = 0
    vector_candidate_count = 0
    embedding_ready_count = 0
    embedding_pending_count = 0

    sorted_rows = sorted(
        rows,
        key=lambda row: (row.law_name.lower(), _section_sort_key(row.section_number), row.section_title.lower(), row.id.lower()),
    )

    for row in sorted_rows:
        record = row.to_record()
        canonical_record = _build_canonical_record(record)
        canonical_doc = build_canonical_retrieval_document(canonical_record)
        canonical_fp = build_retrieval_fingerprint_for_document(canonical_doc)
        stored_doc = _normalize_retrieval_document(row.retrieval_document or "")
        stored_fp = row.retrieval_fingerprint or ""

        has_doc = bool(stored_doc)
        has_fp = bool(stored_fp)
        doc_stale = has_doc and stored_doc != canonical_doc
        fp_stale = has_fp and stored_fp != canonical_fp
        stale = doc_stale or fp_stale
        refresh_needed = (not has_doc) or (not has_fp) or stale

        if row.embedding_status == "ready":
            embedding_ready_count += 1
        else:
            embedding_pending_count += 1

        if stale:
            stale_count += 1
        if not has_doc:
            missing_document_count += 1
        if not has_fp:
            missing_fingerprint_count += 1
        if refresh_needed:
            refresh_needed_count += 1
        if has_doc and has_fp:
            vector_candidate_count += 1

        if refresh_needed and len(sample_records) < limit:
            fingerprint_status = "stale" if stale else ("missing" if not has_fp else "up_to_date")
            sample_records.append({
                "record_id": row.id,
                "citation_label": row.citation_label,
                "law_name": row.law_name,
                "section_number": row.section_number,
                "embedding_status": row.embedding_status or "pending",
                "has_retrieval_document": has_doc,
                "has_retrieval_fingerprint": has_fp,
                "fingerprint_status": fingerprint_status,
                "refresh_needed": refresh_needed,
            })

    if not sample_records:
        for row in sorted_rows[:limit]:
            sample_records.append({
                "record_id": row.id,
                "citation_label": row.citation_label,
                "law_name": row.law_name,
                "section_number": row.section_number,
                "embedding_status": row.embedding_status or "pending",
                "has_retrieval_document": bool(_normalize_retrieval_document(row.retrieval_document or "")),
                "has_retrieval_fingerprint": bool(row.retrieval_fingerprint or ""),
                "fingerprint_status": "up_to_date",
                "refresh_needed": False,
            })

    return {
        "active_source": snapshot.active_source,
        "source_label": snapshot.source_label,
        "database_ready": True,
        "foundation_stage": str(foundation.get("foundation_stage", "database_ready_empty")),
        "persisted_record_count": len(sorted_rows),
        "active_record_count": snapshot.active_record_count,
        "embedding_ready_count": embedding_ready_count,
        "embedding_pending_count": embedding_pending_count,
        "stale_count": stale_count,
        "missing_document_count": missing_document_count,
        "missing_fingerprint_count": missing_fingerprint_count,
        "refresh_needed_count": refresh_needed_count,
        "vector_candidate_count": vector_candidate_count,
        "sample_records": sample_records,
    }


def refresh_persisted_retrieval_metadata(*, force_all: bool = False, limit: int = 12) -> dict[str, object]:
    foundation = get_database_foundation_snapshot()
    session_factory = get_session_factory()
    snapshot = get_legal_source_store_snapshot()

    if not foundation.get("ready") or session_factory is None:
        audit = get_persisted_retrieval_readiness_audit(limit=limit)
        return {
            **audit,
            "refresh_applied": False,
            "refreshed_count": 0,
            "unchanged_count": 0,
            "pending_marked_count": 0,
        }

    refreshed_count = 0
    unchanged_count = 0
    pending_marked_count = 0

    try:
        with session_factory() as session:
            rows = session.scalars(select(LegalSourceORM)).all()
            for row in rows:
                record = row.to_record()
                canonical_record = _build_canonical_record(record)
                canonical_doc = build_canonical_retrieval_document(canonical_record)
                canonical_fp = build_retrieval_fingerprint_for_document(canonical_doc)
                searchable_text = _normalize_retrieval_document(" ".join(canonical_record.searchable_parts))

                stored_doc = _normalize_retrieval_document(row.retrieval_document or "")
                stored_fp = row.retrieval_fingerprint or ""
                has_drift = stored_doc != canonical_doc or stored_fp != canonical_fp
                missing_core = not stored_doc or not stored_fp
                text_drift = _normalize_retrieval_document(row.retrieval_text or "") != searchable_text
                config_gap = not row.embedding_model or not row.embedding_dimensions

                needs_refresh = force_all or has_drift or missing_core or text_drift or config_gap
                if not needs_refresh:
                    unchanged_count += 1
                    continue

                fingerprint_changed = stored_fp != canonical_fp
                row.retrieval_document = canonical_doc
                row.retrieval_fingerprint = canonical_fp
                row.retrieval_text = searchable_text
                row.embedding_model = row.embedding_model or settings.legal_source_embedding_model
                row.embedding_dimensions = row.embedding_dimensions or settings.legal_source_embedding_dimensions
                if fingerprint_changed:
                    if row.embedding_status == "ready":
                        pending_marked_count += 1
                    row.embedding_status = "pending"
                    row.embedding_updated_at = None
                elif not row.embedding_status:
                    row.embedding_status = "pending"

                refreshed_count += 1

            session.commit()
    except SQLAlchemyError:  # pragma: no cover - depends on environment
        audit = get_persisted_retrieval_readiness_audit(limit=limit)
        return {
            **audit,
            "refresh_applied": False,
            "refreshed_count": 0,
            "unchanged_count": 0,
            "pending_marked_count": 0,
        }

    audit = get_persisted_retrieval_readiness_audit(limit=limit)
    return {
        **audit,
        "refresh_applied": refreshed_count > 0 or force_all,
        "refreshed_count": refreshed_count,
        "unchanged_count": unchanged_count,
        "pending_marked_count": pending_marked_count,
    }


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
