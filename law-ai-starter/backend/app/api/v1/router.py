from fastapi import APIRouter

from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.chat import router as chat_router
from app.api.v1.routes.officer_authority import router as officer_authority_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(chat_router, tags=["Chat"])
api_router.include_router(officer_authority_router, tags=["Officer Authority"])