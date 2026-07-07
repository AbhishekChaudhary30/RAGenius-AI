from app.api.document import router as document_router

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import logger
from app.database.database import create_db

from app.api.auth import router as auth_router

from fastapi import Depends

from app.core.security import get_current_user

from app.core.security import (
    get_current_active_user,
    get_admin_user
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting RAGenius AI")

    create_db()

    logger.info("Database Ready")

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