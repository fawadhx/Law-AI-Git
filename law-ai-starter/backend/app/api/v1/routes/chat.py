from fastapi import APIRouter

from app.schemas.chat import ChatQueryRequest, ChatQueryResponse
from app.services.chat_service import generate_mock_legal_response

router = APIRouter()


@router.post("/chat/query", response_model=ChatQueryResponse)
def query_chat(payload: ChatQueryRequest) -> ChatQueryResponse:
    return generate_mock_legal_response(payload.question)