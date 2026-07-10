from app.api.documents import router as document_router

from app.api.embeddings import router as embedding_router

from app.services.embedding_service import EmbeddingService

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import logger
from app.database.database import create_db

from app.api.auth import router as auth_router

from fastapi import Depends

from app.core.security import get_current_user

from app.api.search import router as search_router

from app.api import chat

from app.api.chat import router as chat_router

from app.api.sessions import router as sessions_router

from app.core.security import (
    get_current_active_user,
    get_admin_user
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting RAGenius AI")

    create_db()

    logger.info("Database Ready")
    
    EmbeddingService.get_model()
    
    logger.info("Embedding Model Loaded")

    yield

    logger.info("Stopping RAGenius AI")


app = FastAPI(

    title=settings.APP_NAME,

    version=settings.VERSION,

    description="Enterprise Grade RAG Assistant",

    lifespan=lifespan

)

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


@app.get("/")
def home():

    return {

        "application": settings.APP_NAME,

        "version": settings.VERSION,

        "status": "Running"

    }
    
app.include_router(
    auth_router,
    prefix = settings.API_PREFIX
)

app.include_router(
    document_router,
    prefix = settings.API_PREFIX
)

app.include_router(
    embedding_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    search_router,
    prefix="/api/v1"
)

app.include_router(
    chat.router
)

app.include_router(
    sessions_router
)

@app.get("/me")
def current_user(

    current_user=Depends(
        get_current_active_user
    )

):

    return {

        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "is_admin": current_user.is_admin,
        "is_active": current_user.is_active

    }
    
@app.get("/admin")
def admin_dashboard(

    current_user=Depends(
        get_admin_user
    )

):

    return {

        "message": "Welcome Admin",

        "user": current_user.full_name

    }