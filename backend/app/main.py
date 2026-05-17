from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid

from backend.app.api import (
    auth_routes,
    chat_routes,
    lead_routes,
    dashboard_routes,
    upload_routes,
    workflow_routes
)

from backend.app.api.automation_routes import (
    router as automation_router
)

from backend.app.utils.handlers import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler
)

from backend.app.utils.logger import logger


app = FastAPI(
    title="Smart AI Business Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =========================================
# Exception Handlers
# =========================================

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)


# =========================================
# Logging Middleware
# =========================================

@app.middleware("http")
async def log_requests(request, call_next):

    request_id = str(uuid.uuid4())

    start_time = time.time()

    logger.info(
        f"RequestID: {request_id} | "
        f"Incoming Request | "
        f"Method: {request.method} | "
        f"Path: {request.url.path}"
    )

    response = await call_next(request)

    process_time = round(time.time() - start_time, 4)

    logger.info(
        f"RequestID: {request_id} | "
        f"Completed Request | "
        f"Status: {response.status_code} | "
        f"Time: {process_time}s"
    )

    return response


# =========================================
# Routers
# =========================================

app.include_router(auth_routes.router)
app.include_router(chat_routes.router)
app.include_router(lead_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(upload_routes.router)
app.include_router(workflow_routes.router)

app.include_router(
    automation_router,
    prefix="/automation",
    tags=["Automation"]
)


# =========================================
# Root Endpoint
# =========================================

@app.get("/")
async def root():
    return {
        "message": "AI Business Assistant Running"
    }


# =========================================
# Health Check Endpoint
# =========================================

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }