from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import logger
from app.database.database import create_db


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