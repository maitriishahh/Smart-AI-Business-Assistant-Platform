from fastapi import APIRouter
from pymongo import MongoClient
from backend.app.config.settings import settings

import pandas as pd
import os

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

client = MongoClient(settings.MONGODB_URL)

db = client[settings.DATABASE_NAME]


# =========================================
# ANALYTICS
# =========================================

@router.get("/analytics")
async def get_analytics():

    total_leads = 0

    if os.path.exists("crm_export.csv"):

        crm_df = pd.read_csv(
            "crm_export.csv"
        )

        total_leads = len(crm_df)

    return {
        "total_leads": total_leads,
        "automations_executed": total_leads * 2,
        "crm_exports": total_leads,
        "system_status": {
            "assistant": "active",
            "automation": "active",
            "rag": "active"
        }
    }


# =========================================
# LEADS
# =========================================

@router.get("/leads")
async def get_leads():

    leads_collection = db["leads"]

    all_leads = list(
        leads_collection.find()
    )

    formatted = []

    for lead in all_leads:

        formatted.append({
            "name": lead.get("name"),
            "email": lead.get("email"),
            "company": lead.get("company"),
            "phone": lead.get("phone"),
            "classification": lead.get("classification"),
            "requirements": lead.get("requirements"),
            "created_at": str(
                lead.get("created_at")
            )
        })

    return {
        "leads": formatted
    }


# =========================================
# CHAT LOGS
# =========================================

@router.get("/chat-logs")
async def get_chat_logs():

    conversations = db["conversations"]

    logs = list(
        conversations
        .find()
        .sort("timestamp", -1)
        .limit(50)
    )

    formatted = []

    for log in logs:

        formatted.append({

            "user": log.get(
                "user_message",
                ""
            ),

            "response": log.get(
                "assistant_response",
                ""
            ),

            "timestamp": str(
                log.get(
                    "timestamp",
                    ""
                )
            )
        })

    return {
        "logs": formatted
    }


# =========================================
# DOCUMENTS
# =========================================

@router.get("/documents")
async def get_documents():

    upload_folder = (
        "backend/app/uploads"
    )

    documents = []

    if os.path.exists(upload_folder):

        files = os.listdir(upload_folder)

        for index, file in enumerate(files):

            documents.append({
                "id": index + 1,
                "name": file
            })

    return {
        "documents": documents
    }