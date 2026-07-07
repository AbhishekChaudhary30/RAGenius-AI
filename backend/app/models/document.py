from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Document(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    filename: str
    original_filename: str

    uploaded_by: str

    file_path: str

    file_type: str

    size: int

    status: str = "uploaded"

    created_at: datetime = Field(default_factory=datetime.utcnow)