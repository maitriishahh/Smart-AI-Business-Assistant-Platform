from fastapi import APIRouter
from backend.app.workflows.lead_workflow import (
    lead_capture_pipeline
)

router = APIRouter(
    prefix = "/lead",
    tags=['Lead']
)

@router.get("/")
async def lead_test():
    return{
        "message":"Lead route working"
    }

@router.post("/capture")
async def capture_lead(payload: dict):

    user_message = payload.get("message")

    result = await lead_capture_pipeline(user_message, "test_session")

    return result