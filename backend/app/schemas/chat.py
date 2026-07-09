from pydantic import BaseModel, Field


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


class ChatResponse(BaseModel):

    session_id: str

    question: str

    answer: str

    sources: list[SourceResponse]

    total_sources: int