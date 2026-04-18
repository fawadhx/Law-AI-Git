import logging
from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.errors import AppServiceError, build_error_payload
from app.core.logging import configure_logging
from app.db.bootstrap import initialize_database_foundation

configure_logging(settings)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(
        "Starting %s | version=%s | env=%s | host=%s | port=%s",
        settings.app_name,
        settings.app_version,
        settings.app_env,
        settings.app_host,
        settings.app_port,
    )
    snapshot = initialize_database_foundation()
    logger.info(
        "Database foundation status | mode=%s | ready=%s | stage=%s | persisted_records=%s",
        snapshot.get("mode"),
        snapshot.get("ready"),
        snapshot.get("foundation_stage"),
        snapshot.get("persisted_records"),
    )
    runtime_warnings = settings.runtime_warnings()
    for warning in runtime_warnings:
        logger.warning("Runtime configuration warning | %s", warning)
    yield
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Law AI backend starter scaffold",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": "Law AI backend is running.",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or uuid4().hex[:12]
    request.state.request_id = request_id
    started_at = perf_counter()

    if settings.app_request_logging_enabled:
        logger.info(
            "Request started | method=%s | path=%s | request_id=%s",
            request.method,
            request.url.path,
            request_id,
        )

    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            "Request failed before response | method=%s | path=%s | request_id=%s",
            request.method,
            request.url.path,
            request_id,
        )
        raise

    response.headers["X-Request-ID"] = request_id
    if settings.app_request_logging_enabled:
        duration_ms = round((perf_counter() - started_at) * 1000, 2)
        logger.info(
            "Request completed | method=%s | path=%s | status=%s | duration_ms=%s | request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request_id,
        )
    return response


@app.exception_handler(AppServiceError)
async def handle_app_service_error(request: Request, exc: AppServiceError) -> JSONResponse:
    logger.warning(
        "Handled service error | path=%s | code=%s | detail=%s | request_id=%s",
        request.url.path,
        exc.error_code,
        exc.detail,
        getattr(request.state, "request_id", "unknown"),
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=build_error_payload(
            request=request,
            detail=exc.detail,
            error_code=exc.error_code,
            metadata=exc.metadata,
            boundary_note=exc.boundary_note,
        ),
    )


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    detail = "Request validation failed."
    if request.url.path.startswith("/api/v1/chat"):
        detail = "Please submit a clearer legal-information question before asking for a response."

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=build_error_payload(
            request=request,
            detail=detail,
            error_code="request_validation_failed",
            metadata={"issues": exc.errors()},
        ),
    )


@app.exception_handler(HTTPException)
async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail if isinstance(exc.detail, str) else "Request could not be completed."
    return JSONResponse(
        status_code=exc.status_code,
        content=build_error_payload(
            request=request,
            detail=detail,
            error_code="http_error",
        ),
        headers=exc.headers,
    )


@app.exception_handler(Exception)
async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "Unhandled exception during request | path=%s | request_id=%s",
        request.url.path,
        getattr(request.state, "request_id", "unknown"),
    )
    detail = "The system could not complete this request safely."
    if request.url.path.startswith("/api/v1/chat"):
        detail = (
            "Law AI could not complete this legal-information request safely right now. "
            "Please try again with a narrower factual question."
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=build_error_payload(
            request=request,
            detail=detail,
            error_code="internal_server_error",
        ),
    )
