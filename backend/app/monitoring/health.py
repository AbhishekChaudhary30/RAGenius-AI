from fastapi import APIRouter
from datetime import datetime, UTC
import time

from app.core.config import settings

from sqlmodel import text

from app.database.database import engine
from app.cache.redis_client import RedisClient
from app.services.embedding_service import EmbeddingService

START_TIME = time.time()

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health_check():

    status = {
        "application": "healthy",
        "database": "unknown",
        "redis": "unknown",
        "embedding_model": "unknown"
    }

    # -------------------------
    # Database Health
    # -------------------------

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        status["database"] = "healthy"

    except Exception:

        status["database"] = "unhealthy"

    # -------------------------
    # Redis Health
    # -------------------------

    try:

        if RedisClient.is_connected():

            RedisClient.set_json(
                "health_check",
                {"ok": True},
                ttl=30
            )

            value = RedisClient.get_json(
                "health_check"
            )

            if value is not None:

                status["redis"] = "healthy"

            else:

                status["redis"] = "unhealthy"

        else:

            status["redis"] = "disconnected"

    except Exception:

        status["redis"] = "unhealthy"

    # -------------------------
    # Embedding Model
    # -------------------------

    try:

        EmbeddingService.get_model()

        status["embedding_model"] = "loaded"

    except Exception:

        status["embedding_model"] = "failed"

    # -------------------------
    # Overall Status
    # -------------------------

    overall = "healthy"

    for value in status.values():

        if value not in ["healthy", "loaded"]:

            overall = "degraded"

            break

    return {

        "status": overall,

        "services": status

    }
    
@router.get("/summary")
def monitoring_summary():

    uptime_seconds = round(
        time.time() - START_TIME,
        2
    )

    return {

        "application": settings.APP_NAME,

        "version": settings.VERSION,

        "environment": "development",

        "server_time": datetime.now(
            UTC
        ).isoformat(),

        "uptime_seconds": uptime_seconds,

        "redis_connected": RedisClient.is_connected(),

        "embedding_loaded": (
            EmbeddingService._model
            is not None
        )

    }