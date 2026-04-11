from fastapi import APIRouter

from app.schemas.chat import ChatQueryRequest, ChatQueryResponse
from app.services.chat_service import build_mock_chat_response

router = APIRouter()


@router.post("/query", response_model=ChatQueryResponse)
def query_law_assistant(payload: ChatQueryRequest) -> ChatQueryResponse:
    return build_mock_chat_response(payload.question)
