from pydantic import BaseModel

from typing import List


class ChatMessage(BaseModel):

    role: str

    content: str


class ConversationMemory(BaseModel):

    session_id: str

    messages: List[ChatMessage] = []