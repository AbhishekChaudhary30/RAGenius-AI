import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        request_id = str(uuid.uuid4())[:8]

        start = time.perf_counter()

        logger.info(
            f"[{request_id}] "
            f"Started {request.method} {request.url.path}"
        )

        try:
            response = await call_next(
                request
            )
            
        except Exception:
            logger.exception(
                f"[{request_id}] Request Failed"
            )
            raise
        
        elapsed = round(
            time.perf_counter() - start,
            4
        )

        logger.info(
            f"[{request_id}] "
            f"Completed "
            f"Status={response.status_code} "
            f"Time={elapsed}s"
        )

        response.headers["X-Request-ID"] = request_id

        return response