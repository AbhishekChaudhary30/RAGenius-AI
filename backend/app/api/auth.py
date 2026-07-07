from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database.session import get_session
from app.schemas.user import UserRegister, UserResponse
from app.services.auth_service import create_user

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