from collections.abc import Generator
from functools import lru_cache
from urllib.parse import urlparse

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


@lru_cache(maxsize=1)
def get_engine() -> Engine | None:
    if not settings.database_url:
        return None

    connect_args: dict[str, object] = {}
    pool_size = settings.database_pool_size
    max_overflow = settings.database_max_overflow
    parsed = urlparse(settings.database_url)

    if parsed.scheme.startswith("postgresql") or parsed.scheme.startswith("postgres"):
        connect_args["connect_timeout"] = settings.database_connect_timeout_seconds

    return create_engine(
        settings.database_url,
        echo=settings.database_echo,
        pool_pre_ping=settings.database_pool_pre_ping,
        pool_size=pool_size,
        max_overflow=max_overflow,
        connect_args=connect_args,
    )


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session] | None:
    engine = get_engine()
    if engine is None:
        return None
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    session_factory = get_session_factory()
    if session_factory is None:
        raise RuntimeError("DATABASE_URL is not configured for this environment.")

    db = session_factory()
    try:
        yield db
    finally:
        db.close()


def get_database_status() -> dict[str, object]:
    configured = bool(settings.database_url)
    if not configured:
        return {
            "configured": False,
            "ready": False,
            "mode": "in_memory",
            "detail": "DATABASE_URL is empty, so the app is still running in in-memory prototype mode.",
        }

    engine = get_engine()
    if engine is None:
        return {
            "configured": True,
            "ready": False,
            "mode": "database_unavailable",
            "detail": "Database engine could not be created from the current DATABASE_URL.",
        }

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "configured": True,
            "ready": True,
            "mode": "database_ready",
            "detail": "Database connection is healthy and ready for table initialization or persistence work.",
        }
    except Exception as exc:  # pragma: no cover - depends on environment
        return {
            "configured": True,
            "ready": False,
            "mode": "database_unavailable",
            "detail": f"Database connection failed: {exc}",
        }
