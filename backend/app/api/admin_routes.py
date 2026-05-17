from fastapi import APIRouter
from pymongo import MongoClient
from backend.app.config.settings import settings

import pandas as pd
import os
from datetime import datetime
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

    # =========================================
    # LEADS COUNT
    # =========================================

    leads_count = (
        db["leads"]
        .count_documents({})
    )

    # =========================================
    # CONVERSATIONS COUNT
    # =========================================

    conversations_count = (
        db["conversations"]
        .count_documents({})
    )

    # =========================================
    # AUTOMATIONS COUNT
    # =========================================

    automations_run = (
        db["automation_logs"]
        .count_documents({})
    )

    # =========================================
    # UPLOADED DOCUMENTS COUNT
    # =========================================

    upload_folder = os.path.join(
        os.getcwd(),
        "backend",
        "app",
        "uploads"
    )

    uploaded_docs = 0

    if os.path.exists(upload_folder):

        for root, dirs, files in os.walk(
            upload_folder
        ):

            pdf_files = [

                file for file in files

                if file.endswith(".pdf")
            ]

            uploaded_docs += len(pdf_files)

    print("TOTAL PDFs:", uploaded_docs)

    # =========================================
    # RETURN ANALYTICS
    # =========================================

    return {

        "total_leads":
            leads_count,

        "total_conversations":
            conversations_count,

        "uploaded_documents":
            uploaded_docs,

        "crm_syncs":
            leads_count,

        "automations_run":
            automations_run
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

    documents_collection = db["documents"]

    docs = list(
        documents_collection
        .find()
        .sort("uploaded_at", -1)
    )

    formatted = []

    for index, doc in enumerate(docs):

        formatted.append({

            "id": index + 1,

            "name":
                doc.get(
                    "original_filename"
                ),

            "path":
                doc.get("path"),

            "uploaded_at": str(
                doc.get(
                    "uploaded_at"
                )
            )
        })

    return {
        "documents": formatted
    }