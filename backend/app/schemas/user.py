from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):

    full_name: str

    email: EmailStr

    password: str


class UserLogin(BaseModel):

    email: EmailStr

    password: str


class UserResponse(BaseModel):

    id: int

    full_name: str

    email: EmailStr

    is_active: bool

    is_admin: bool

    created_at: datetime


class Token(BaseModel):

    access_token: str

    token_type: str = "bearer"