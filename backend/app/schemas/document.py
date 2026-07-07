from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class DocumentResponse(SQLModel):
    id: int
    filename: str
    original_filename: str
    uploaded_by: str
    size: int
    file_type: str
    status: str
    created_at: datetime


class DocumentList(SQLModel):
    id: int
    filename: str
    original_filename: str
    size: int
    status: str
    created_at: datetime