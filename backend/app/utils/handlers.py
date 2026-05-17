from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from backend.app.utils.logger import logger


# ----------------------------------------
# HTTP Exception Handler
# ----------------------------------------

async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    logger.warning(
        f"HTTP Exception | "
        f"Path: {request.url.path} | "
        f"Status: {exc.status_code} | "
        f"Detail: {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


# ----------------------------------------
# Validation Exception Handler
# ----------------------------------------

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    logger.error(
        f"Validation Error | "
        f"Path: {request.url.path} | "
        f"Errors: {exc.errors()}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation Error",
            "details": exc.errors()
        }
    )


# ----------------------------------------
# Global Exception Handler
# ----------------------------------------

async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.error(
        f"Unhandled Exception | "
        f"Path: {request.url.path} | "
        f"Error: {str(exc)}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error"
        }
    )