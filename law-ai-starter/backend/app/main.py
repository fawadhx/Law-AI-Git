import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.bootstrap import initialize_database_foundation

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Law AI backend starter scaffold",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
def startup_event() -> None:
    snapshot = initialize_database_foundation()
    logger.info(
        "Database foundation status | mode=%s | ready=%s | stage=%s | persisted_records=%s",
        snapshot.get("mode"),
        snapshot.get("ready"),
        snapshot.get("foundation_stage"),
        snapshot.get("persisted_records"),
    )


@app.get("/")
def root():
    return {"message": "Law AI backend is running."}
