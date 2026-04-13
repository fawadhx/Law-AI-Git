from sqlalchemy import delete, func, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.data.legal_sources import LEGAL_SOURCES
from app.db.base import Base
from app.db.models import LegalSourceORM
from app.db.session import get_database_status, get_engine, get_session_factory


def create_database_tables() -> dict[str, object]:
    status = get_database_status()
    engine = get_engine()
    if not status["configured"] or engine is None:
        return {**status, "tables_created": False}

    Base.metadata.create_all(bind=engine)
    return {**status, "tables_created": True}


def bootstrap_legal_sources(*, force_refresh: bool = False) -> dict[str, object]:
    status = get_database_status()
    session_factory = get_session_factory()
    if not status["ready"] or session_factory is None:
        return {**status, "bootstrapped": False, "persisted_records": 0}

    persisted_records = 0
    imported_records = 0

    with session_factory() as session:
        if force_refresh:
            session.execute(delete(LegalSourceORM))
            session.commit()

        persisted_records = int(session.scalar(select(func.count()).select_from(LegalSourceORM)) or 0)
        if persisted_records and not force_refresh:
            return {
                **status,
                "bootstrapped": False,
                "persisted_records": persisted_records,
                "imported_records": 0,
                "detail": "Database already contains legal source rows, so bootstrap was skipped.",
            }

        for record in LEGAL_SOURCES:
            session.merge(LegalSourceORM.from_record(record))
            imported_records += 1

        session.commit()
        persisted_records = int(session.scalar(select(func.count()).select_from(LegalSourceORM)) or 0)

    return {
        **status,
        "bootstrapped": True,
        "persisted_records": persisted_records,
        "imported_records": imported_records,
        "detail": "Legal source records were synchronized from the in-memory prototype catalog into the database foundation.",
    }


def get_database_foundation_snapshot() -> dict[str, object]:
    status = get_database_status()
    session_factory = get_session_factory()
    if not status["ready"] or session_factory is None:
        return {
            **status,
            "persisted_records": 0,
            "table_name": LegalSourceORM.__tablename__,
            "foundation_stage": "in_memory_only" if not status["configured"] else "database_not_ready",
        }

    try:
        with session_factory() as session:
            persisted_records = int(session.scalar(select(func.count()).select_from(LegalSourceORM)) or 0)
        return {
            **status,
            "persisted_records": persisted_records,
            "table_name": LegalSourceORM.__tablename__,
            "foundation_stage": "database_seeded" if persisted_records else "database_ready_empty",
        }
    except SQLAlchemyError as exc:  # pragma: no cover - depends on environment
        return {
            **status,
            "persisted_records": 0,
            "table_name": LegalSourceORM.__tablename__,
            "foundation_stage": "database_error",
            "detail": f"Database foundation check failed: {exc}",
        }


def initialize_database_foundation() -> dict[str, object]:
    status = get_database_status()
    if not status["configured"]:
        return {
            **status,
            "tables_created": False,
            "bootstrapped": False,
            "persisted_records": 0,
            "foundation_stage": "in_memory_only",
        }

    create_result = create_database_tables() if settings.database_auto_create_tables else {**status, "tables_created": False}
    bootstrap_result = {
        **status,
        "bootstrapped": False,
        "persisted_records": 0,
        "imported_records": 0,
    }

    if settings.database_bootstrap_legal_sources:
        bootstrap_result = bootstrap_legal_sources(force_refresh=settings.database_bootstrap_force_refresh)

    snapshot = get_database_foundation_snapshot()
    return {
        **snapshot,
        "tables_created": bool(create_result.get("tables_created", False)),
        "bootstrapped": bool(bootstrap_result.get("bootstrapped", False)),
        "imported_records": int(bootstrap_result.get("imported_records", 0) or 0),
    }
