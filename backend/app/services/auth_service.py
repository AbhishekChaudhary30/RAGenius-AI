from sqlmodel import Session, select

from app.models.user import User
from app.schemas.user import UserRegister
from app.core.security import hash_password

from app.core.security import verify_password

def create_user(
    session: Session,
    user: UserRegister
):

    existing_user = session.exec(
        select(User).where(
            User.email == user.email
        )
    ).first()

    if existing_user:

        return None

    db_user = User(

        full_name=user.full_name,

        email=user.email,

        hashed_password=hash_password(
            user.password
        )

    )

    session.add(db_user)

    session.commit()

    session.refresh(db_user)

    return db_user

def authenticate_user(session, email: str, password: str):

    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user