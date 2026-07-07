from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    full_name: str

    email: str = Field(index=True, unique=True)

    hashed_password: str

    is_active: bool = True

    is_admin: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)