from fastapi import APIRouter

from pydantic import BaseModel

from app.services.rag_service import RAGService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):

    question: str

    top_k: int = 5


@router.post("/")
def chat(
    request: ChatRequest
):

    return RAGService.ask(

        question=request.question,

        top_k=request.top_k

    )