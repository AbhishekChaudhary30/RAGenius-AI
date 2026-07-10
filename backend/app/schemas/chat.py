from pydantic import BaseModel, Field

from typing import Any

class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="User question"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20
    )

    session_id: str | None = Field(
        default=None,
        description="Existing session id. Leave empty to create a new session."
    )


class SourceResponse(BaseModel):

    filename: str

    chunk_index: int
    

class MetricsResponse(BaseModel):
    retrieval_time_sec: float
    generation_time_sec: float
    total_time_sec: float
    context_length: int
    history_length: int
    total_sources: int
    provider: str


class ChatResponse(BaseModel):

    session_id: str

    question: str

    answer: str

    sources: list[dict[str, Any]]

    total_sources: int
    
    history_messages: int
    
    metrics: MetricsResponse