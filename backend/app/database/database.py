import app.models

import app.models.document

from pathlib import Path

from sqlmodel import SQLModel, create_engine

from app.core.config import settings

db_path = Path("data/database")

db_path.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={
        "check_same_thread": False
    }
)


def create_db():

    SQLModel.metadata.create_all(engine)