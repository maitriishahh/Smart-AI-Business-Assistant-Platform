import os
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: %(message)s:'
)

project_name = "business_ai_automation_platform"

list_of_files = [

    # =========================
    # ROOT LEVEL
    # =========================
    ".env",
    ".gitignore",
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml",
    "README.md",

    # =========================
    # BACKEND
    # =========================
    "backend/__init__.py",

    # APP
    "backend/app/__init__.py",
    "backend/app/main.py",

    # =========================
    # API ROUTES
    # =========================
    "backend/app/api/__init__.py",
    "backend/app/api/auth_routes.py",
    "backend/app/api/chat_routes.py",
    "backend/app/api/lead_routes.py",
    "backend/app/api/dashboard_routes.py",
    "backend/app/api/upload_routes.py",
    "backend/app/api/workflow_routes.py",

    # =========================
    # AGENTS
    # =========================
    "backend/app/agents/__init__.py",
    "backend/app/agents/planner_agent.py",
    "backend/app/agents/executor_agent.py",
    "backend/app/agents/validator_agent.py",
    "backend/app/agents/orchestrator.py",
    "backend/app/agents/prompts.py",

    # =========================
    # RAG PIPELINE
    # =========================
    "backend/app/rag/__init__.py",
    "backend/app/rag/chunking.py",
    "backend/app/rag/embeddings.py",
    "backend/app/rag/retriever.py",
    "backend/app/rag/vector_store.py",
    "backend/app/rag/document_loader.py",

    # =========================
    # MEMORY
    # =========================
    "backend/app/memory/__init__.py",
    "backend/app/memory/short_term.py",
    "backend/app/memory/long_term.py",
    "backend/app/memory/conversation_history.py",

    # =========================
    # AUTOMATIONS
    # =========================
    "backend/app/automations/__init__.py",
    "backend/app/automations/email_summary.py",
    "backend/app/automations/followup_generator.py",
    "backend/app/automations/crm_sync.py",

    # =========================
    # WORKFLOWS
    # =========================
    "backend/app/workflows/__init__.py",
    "backend/app/workflows/chat_workflow.py",
    "backend/app/workflows/lead_workflow.py",
    "backend/app/workflows/automation_workflow.py",

    # =========================
    # DATABASE
    # =========================
    "backend/app/database/__init__.py",
    "backend/app/database/mongodb.py",
    "backend/app/database/collections.py",

    # =========================
    # MODELS
    # =========================
    "backend/app/models/__init__.py",
    "backend/app/models/user_model.py",
    "backend/app/models/chat_model.py",
    "backend/app/models/lead_model.py",
    "backend/app/models/document_model.py",
    "backend/app/models/workflow_model.py",

    # =========================
    # AUTH
    # =========================
    "backend/app/auth/__init__.py",
    "backend/app/auth/jwt_handler.py",
    "backend/app/auth/hashing.py",
    "backend/app/auth/dependencies.py",

    # =========================
    # SERVICES
    # =========================
    "backend/app/services/__init__.py",
    "backend/app/services/chat_service.py",
    "backend/app/services/lead_service.py",
    "backend/app/services/dashboard_service.py",
    "backend/app/services/document_service.py",

    # =========================
    # UTILS
    # =========================
    "backend/app/utils/__init__.py",
    "backend/app/utils/logger.py",
    "backend/app/utils/retry.py",
    "backend/app/utils/helpers.py",

    # =========================
    # CONFIG
    # =========================
    "backend/app/config/__init__.py",
    "backend/app/config/settings.py",

    # =========================
    # DASHBOARD
    # =========================
    "dashboard/streamlit_app.py",
    "dashboard/pages/analytics.py",
    "dashboard/pages/leads.py",
    "dashboard/pages/chat_logs.py",
    "dashboard/pages/workflows.py",

    # =========================
    # DOCS
    # =========================
    "docs/architecture.md",
    "docs/api_documentation.md"
]


for filepath in list_of_files:

    filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

        logging.info(
            f"Creating directory: {filedir} for the file: {filename}"
        )

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):

        with open(filepath, 'w') as f:
            pass

        logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} already exists")

