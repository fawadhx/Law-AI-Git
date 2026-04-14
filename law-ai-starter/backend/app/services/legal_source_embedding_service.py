from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import datetime
from typing import Any
from urllib import error, request

from sqlalchemy import select

from app.core.config import settings
from app.db.models import LegalSourceEmbeddingORM, LegalSourceORM
from app.db.session import get_database_status, get_session_factory

EMBEDDINGS_API_URL = "https://api.openai.com/v1/embeddings"
DEFAULT_EMBEDDING_RUN_LIMIT = 10


def _provider_ready() -> bool:
    return bool(settings.openai_api_key and settings.legal_source_embedding_model)


def is_embedding_provider_ready() -> bool:
    return _provider_ready()


def _clean_embedding_input(text: str | None) -> str:
    return " ".join((text or "").split()).strip()


def _needs_embedding_run(record: LegalSourceORM, embedding_row: LegalSourceEmbeddingORM | None) -> bool:
    if not record.retrieval_document or not record.retrieval_fingerprint:
        return False
    if record.embedding_status != "ready":
        return True
    if embedding_row is None:
        return True
    if embedding_row.source_fingerprint != record.retrieval_fingerprint:
        return True
    if embedding_row.model_name != settings.legal_source_embedding_model:
        return True
    if embedding_row.dimensions != settings.legal_source_embedding_dimensions:
        return True
    if embedding_row.vector_length() <= 0:
        return True
    return False


def _fingerprint_match(record: LegalSourceORM, embedding_row: LegalSourceEmbeddingORM | None) -> bool:
    return bool(
        embedding_row
        and record.retrieval_fingerprint
        and embedding_row.source_fingerprint == record.retrieval_fingerprint
    )


def _vector_ready(record: LegalSourceORM, embedding_row: LegalSourceEmbeddingORM | None) -> bool:
    return bool(
        record.embedding_status == "ready"
        and embedding_row is not None
        and embedding_row.vector_length() > 0
        and _fingerprint_match(record, embedding_row)
        and embedding_row.model_name == settings.legal_source_embedding_model
        and embedding_row.dimensions == settings.legal_source_embedding_dimensions
    )


def generate_text_embedding(text: str) -> list[float]:
    payload = json.dumps(
        {
            "model": settings.legal_source_embedding_model,
            "input": text,
        }
    ).encode("utf-8")
    req = request.Request(
        EMBEDDINGS_API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Embedding API error {exc.code}: {details or exc.reason}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Embedding API connection failed: {exc.reason}") from exc

    data = body.get("data") or []
    if not data or not isinstance(data[0], dict):
        raise RuntimeError("Embedding API returned no embedding data.")

    embedding = data[0].get("embedding")
    if not isinstance(embedding, list) or not embedding:
        raise RuntimeError("Embedding API returned an empty embedding vector.")

    return [float(value) for value in embedding]


def get_embedding_store_snapshot(sample_limit: int = 12) -> dict[str, Any]:
    status = get_database_status()
    session_factory = get_session_factory()
    provider_ready = _provider_ready()

    empty = {
        "provider_ready": provider_ready,
        "api_key_configured": bool(settings.openai_api_key),
        "database_ready": bool(status.get("ready")),
        "persisted_record_count": 0,
        "vector_row_count": 0,
        "ready_vector_count": 0,
        "pending_count": 0,
        "error_count": 0,
        "runnable_count": 0,
        "sample_records": [],
        "workflow_note": "Database is not ready yet, so embedding storage is unavailable.",
    }
    if not status.get("ready") or session_factory is None:
        return empty

    with session_factory() as session:
        records = list(session.scalars(select(LegalSourceORM)).all())
        embedding_rows = {
            row.record_id: row for row in session.scalars(select(LegalSourceEmbeddingORM)).all()
        }

        sample_records: list[dict[str, Any]] = []
        ready_vector_count = 0
        pending_count = 0
        error_count = 0
        runnable_count = 0

        for record in records:
            row = embedding_rows.get(record.record_id)
            ready = _vector_ready(record, row)
            runnable = _needs_embedding_run(record, row)

            if ready:
                ready_vector_count += 1
            elif record.embedding_status == "error":
                error_count += 1
            else:
                pending_count += 1

            if runnable:
                runnable_count += 1

            if len(sample_records) < sample_limit and (runnable or record.embedding_status == "error"):
                sample_records.append(
                    {
                        "record_id": record.record_id,
                        "citation_label": record.citation_label,
                        "law_name": record.law_name,
                        "section_number": record.section_number,
                        "embedding_status": record.embedding_status,
                        "has_vector": bool(row and row.vector_length() > 0),
                        "fingerprint_match": _fingerprint_match(record, row),
                        "model_name": row.model_name if row else None,
                        "dimensions": row.dimensions if row else None,
                        "refresh_needed": runnable,
                        "last_error": row.last_error if row else None,
                    }
                )

    note = (
        "OpenAI API key is configured, so persisted legal-source embeddings can now be generated into the database-backed vector store."
        if provider_ready
        else "OpenAI API key is missing, so embedding generation stays unavailable even though the database audit is ready."
    )

    return {
        "provider_ready": provider_ready,
        "api_key_configured": bool(settings.openai_api_key),
        "database_ready": True,
        "persisted_record_count": len(records),
        "vector_row_count": len(embedding_rows),
        "ready_vector_count": ready_vector_count,
        "pending_count": pending_count,
        "error_count": error_count,
        "runnable_count": runnable_count,
        "sample_records": sample_records,
        "workflow_note": note,
    }


def run_embedding_generation(*, limit: int | None = None, record_ids: Sequence[str] | None = None) -> dict[str, Any]:
    status = get_database_status()
    session_factory = get_session_factory()
    provider_ready = _provider_ready()
    effective_limit = max(1, int(limit or DEFAULT_EMBEDDING_RUN_LIMIT))

    if not status.get("ready") or session_factory is None:
        snapshot = get_embedding_store_snapshot()
        return {
            "run_attempted": False,
            "processed_count": 0,
            "success_count": 0,
            "error_count": 0,
            "skipped_count": 0,
            **snapshot,
        }

    if not provider_ready:
        snapshot = get_embedding_store_snapshot()
        return {
            "run_attempted": False,
            "processed_count": 0,
            "success_count": 0,
            "error_count": 0,
            "skipped_count": 0,
            **snapshot,
        }

    target_ids = set(record_ids or [])

    with session_factory() as session:
        all_records = list(session.scalars(select(LegalSourceORM)).all())
        embedding_rows = {
            row.record_id: row for row in session.scalars(select(LegalSourceEmbeddingORM)).all()
        }

        candidates: list[tuple[LegalSourceORM, LegalSourceEmbeddingORM | None]] = []
        for record in all_records:
            if target_ids and record.record_id not in target_ids:
                continue
            embedding_row = embedding_rows.get(record.record_id)
            if _needs_embedding_run(record, embedding_row):
                candidates.append((record, embedding_row))

        processed_count = 0
        success_count = 0
        error_count = 0
        skipped_count = 0

        for record, embedding_row in candidates[:effective_limit]:
            text = _clean_embedding_input(record.retrieval_document)
            if not text:
                skipped_count += 1
                continue

            processed_count += 1
            try:
                vector = generate_text_embedding(text)
                if embedding_row is None:
                    embedding_row = LegalSourceEmbeddingORM(
                        record_id=record.record_id,
                        model_name=settings.legal_source_embedding_model,
                        dimensions=len(vector),
                        source_fingerprint=record.retrieval_fingerprint or "",
                        embedding=vector,
                        last_error=None,
                    )
                    session.add(embedding_row)
                else:
                    embedding_row.model_name = settings.legal_source_embedding_model
                    embedding_row.dimensions = len(vector)
                    embedding_row.source_fingerprint = record.retrieval_fingerprint or ""
                    embedding_row.embedding = vector
                    embedding_row.last_error = None
                    embedding_row.updated_at = datetime.utcnow()

                record.embedding_status = "ready"
                record.embedding_model = settings.legal_source_embedding_model
                record.embedding_dimensions = len(vector)
                record.embedding_updated_at = datetime.utcnow()
                success_count += 1
            except Exception as exc:  # noqa: BLE001
                if embedding_row is None:
                    embedding_row = LegalSourceEmbeddingORM(
                        record_id=record.record_id,
                        model_name=settings.legal_source_embedding_model,
                        dimensions=settings.legal_source_embedding_dimensions,
                        source_fingerprint=record.retrieval_fingerprint or "",
                        embedding=None,
                        last_error=str(exc),
                    )
                    session.add(embedding_row)
                else:
                    embedding_row.last_error = str(exc)
                    embedding_row.updated_at = datetime.utcnow()

                record.embedding_status = "error"
                error_count += 1

        session.commit()

    snapshot = get_embedding_store_snapshot()
    return {
        "run_attempted": True,
        "processed_count": processed_count,
        "success_count": success_count,
        "error_count": error_count,
        "skipped_count": skipped_count,
        **snapshot,
    }
