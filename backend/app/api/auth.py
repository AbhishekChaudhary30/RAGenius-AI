from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.database.session import get_session
from app.schemas.user import UserRegister, UserResponse
from app.services.auth_service import create_user

from app.core.security import create_access_token
from app.services.auth_service import authenticate_user
from app.schemas.user import UserLogin, Token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserRegister,
    session: Session = Depends(get_session)
):

    db_user = create_user(
        session=session,
        user=user
    )

    if db_user is None:
        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    return db_user

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):

    db_user = authenticate_user(
        session,
        form_data.username,
        form_data.password
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }