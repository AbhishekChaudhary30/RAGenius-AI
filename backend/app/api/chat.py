from fastapi import APIRouter

from app.utils.sse import format_sse

from fastapi.responses import StreamingResponse

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.services.rag_service import RAGService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest
):

    return RAGService.ask(

        question=request.question,

        top_k=request.top_k,

        session_id=request.session_id

    )
    
@router.post(
    "/stream"
)
def stream_chat(
    request: ChatRequest
):

    def event_generator():

        for event in RAGService.stream_events(

            question=request.question,

            top_k=request.top_k,

            session_id=request.session_id

        ):

            yield format_sse(

                event["event"],

                event["data"]

            )

    return StreamingResponse(

        event_generator(),

        media_type="text/event-stream",

        headers={

            "Cache-Control": "no-cache",

            "Connection": "keep-alive"

        }

    )