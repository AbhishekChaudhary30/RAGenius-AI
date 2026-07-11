from fastapi import APIRouter, Request, HTTPException

from app.utils.sse import format_sse

from fastapi.responses import StreamingResponse

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.services.rag_service import RAGService
from app.security.rate_limiter import RateLimiter

from app.security.input_validator import InputValidator
from app.security.prompt_guard import PromptGuard


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    http_request: Request
):
    
    client_ip = http_request.client.host
    
    if not RateLimiter.allow_request(
        client_ip
    ):
        raise HTTPException(
            status_code=429,
            detail = "Rate limit exceeded. Please try again later."
        )
        
    question = InputValidator.validate_question(
        request.question
    )
    
    if not PromptGuard.is_safe(
        question
    ):
        
        raise HTTPException(
            status_code=4000,
            detail = "Unsafe prompt detected."
        )

    return RAGService.ask(

        question=question,

        top_k=request.top_k,

        session_id=request.session_id

    )
    
@router.post(
    "/stream"
)
def stream_chat(
    request: ChatRequest,
    http_request: Request
):
    
    client_ip = http_request.client.host
    
    if not RateLimiter.allow_request(
        client_ip
    ):
        raise HTTPException(
            status_code=429,
            detail = "Rate limit excedded. Please try again later."
        )
        
    question = InputValidator.validate_question(
        request.question
    )
    
    if not PromptGuard.is_safe(
        question
    ):
        raise HTTPException(
            status_code=400,
            detail="Unsafe prompt detected."
        )

    def event_generator():

        for event in RAGService.stream_events(

            question=question,

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