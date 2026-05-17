from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, UTC
from backend.app.automations.email_summary import summarize_email
from backend.app.automations.crm_sync import sync_lead_to_crm
from backend.app.automations.followup_generator import generate_followup 

router = APIRouter()


class EmailRequest(BaseModel):
    email_content: str

class CRMLeadRequest(BaseModel):
    name: str
    email: str
    company: str
    phone: str
    requirements: str
    priority: str

class FollowupRequest(BaseModel):
    name: str
    company: str
    requirements: str
    classification: str
    followup_type: str = "general"

@router.post("/email/summarize")
async def summarize_email_route(request: EmailRequest):

    result = await summarize_email(request.email_content)

    return {
        "success": True,
        "data": result,
        "generated_at":datetime.now(UTC).isoformat()
    }

@router.post("/crm/sync")
async def crm_sync_route(request: CRMLeadRequest):

    result = await sync_lead_to_crm(
        request.model_dump()
    )

    return {
        "success": True,
        "data": result
    }

@router.post("/followup/generate")
async def followup_route(request: FollowupRequest):

    lead_data = request.model_dump()

    followup_type = lead_data.pop("followup_type")
    result = await generate_followup(
        lead_data, followup_type
    )

    return {
        "success": True,
        "data": result
    }