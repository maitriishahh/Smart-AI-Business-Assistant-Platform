from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, UTC
from backend.app.automations.email_summary import summarize_email
from backend.app.automations.crm_sync import sync_lead_to_crm
from backend.app.automations.followup_generator import generate_followup 
from backend.app.database.mongodb import database

router = APIRouter()

db = database

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
    await db["automation_logs"].insert_one({

    "type": "email_summary",

    "timestamp": datetime.now(UTC)
})
    
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

@router.get("/crm/records")
async def get_crm_records():

    cursor = (
        db["leads"]
        .find()
        .sort("created_at", -1)
    )

    formatted = []

    async for record in cursor:

        formatted.append({

            "name":
                record.get("name"),

            "email":
                record.get("email"),

            "company":
                record.get("company"),

            "phone":
                record.get("phone"),

            "requirements":
                record.get("requirements"),

            "priority":
                record.get("priority"),

            "timestamp":
                str(
                    record.get(
                        "created_at",
                        ""
                    )
                )
        })

    return {
        "records": formatted
    }

@router.post("/followup/generate")
async def followup_route(request: FollowupRequest):

    lead_data = request.model_dump()

    followup_type = lead_data.pop(
        "followup_type"
    )

    result = await generate_followup(
        lead_data,
        followup_type
    )

    await db["automation_logs"].insert_one({

        "type": "followup_generation",

        "timestamp": datetime.now(UTC)
    })

    return {
        "success": True,
        "data": result
    }