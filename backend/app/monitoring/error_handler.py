import traceback

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logging import logger


async def global_exception_handler(
    request: Request,
    exc: Exception
):

    logger.error(
        "Unhandled Exception"
    )

    logger.error(
        traceback.format_exc()
    )

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "error": "Internal Server Error",

            "message": "Something went wrong. Please try again later."

        }

    )