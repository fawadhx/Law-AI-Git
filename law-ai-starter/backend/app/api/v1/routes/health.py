from datetime import datetime, timezone

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.session import get_database_status

router = APIRouter()


@router.get("/health")
def health_check():
    database = get_database_status()
    warnings = settings.runtime_warnings()

    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "time": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "readiness_requirements": {
            "database": settings.app_readiness_requires_database,
            "openai": settings.app_readiness_requires_openai,
        },
        "warnings": warnings,
    }


@router.get("/health/live")
def health_live():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }


@router.get("/health/ready")
def health_ready():
    database = get_database_status()
    openai_ready = bool(settings.openai_api_key)

    readiness_checks = {
        "database": {
            "required": settings.app_readiness_requires_database,
            "ready": database["ready"],
            "detail": database["detail"],
        },
        "openai": {
            "required": settings.app_readiness_requires_openai,
            "ready": openai_ready,
            "detail": "OpenAI API key is configured." if openai_ready else "OPENAI_API_KEY is not configured.",
        },
    }

    ready = True
    if settings.app_readiness_requires_database and not database["ready"]:
        ready = False
    if settings.app_readiness_requires_openai and not openai_ready:
        ready = False

    payload = {
        "status": "ready" if ready else "not_ready",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "checks": readiness_checks,
        "warnings": settings.runtime_warnings(),
    }
    status_code = status.HTTP_200_OK if ready else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(status_code=status_code, content=payload)
