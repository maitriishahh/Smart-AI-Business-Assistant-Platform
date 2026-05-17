import re
from datetime import datetime, UTC

from backend.app.database.collections import (
    lead_collection
)


# =========================
# LEAD INTENT DETECTION
# =========================

def detect_lead_intent(message: str):

    message = message.lower().strip()

    # =========================================
    # HIGH-INTENT LEAD KEYWORDS
    # =========================================

    lead_keywords = [

        # Hiring / service interest
        "hire",
        "hiring",
        "interested in",
        "need your service",
        "interested in your service",
        "interested in working",
        "work with you",
        "looking for services",
        "consultation",
        "book a call",
        "schedule a call",
        "contact me",
        "get in touch",

        # Contact sharing
        "my email is",
        "my phone number is",
        "my company is",

        # Business inquiry
        "request a quote",
        "business inquiry",
        "partnership",
        "collaboration",

        # Explicit lead actions
        "i want to proceed",
        "let's discuss",
        "reach out to me"
    ]

    # =========================================
    # NEGATIVE FILTERS
    # Prevent RAG questions from becoming leads
    # =========================================

    negative_keywords = [
        "pricing",
        "services",
        "summarize",
        "summary",
        "explain",
        "pdf",
        "document",
        "uploaded file",
        "what does",
        "tell me about",
        "information",
        "details",
        "content",
        "analysis",
        "report"
    ]

    # If message looks informational → NOT lead intent
    if any(keyword in message for keyword in negative_keywords):
        return False

    # =========================================
    # POSITIVE LEAD DETECTION
    # =========================================

    return any(keyword in message for keyword in lead_keywords)


# =========================
# EMAIL EXTRACTION
# =========================

def extract_email(text):

    pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


# =========================
# NAME EXTRACTION
# =========================

def extract_name(text):

    patterns = [
        r"I'm\s+([A-Za-z ]+)",
        r"I am\s+([A-Za-z ]+)",
        r"My name is\s+([A-Za-z ]+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


# =========================
# COMPANY EXTRACTION
# =========================

def extract_company(text):

    patterns = [
         r"from\s+([A-Za-z0-9 &]+?)(?:\.|,|and|$)",
    r"at\s+([A-Za-z0-9 &]+?)(?:\.|,|and|$)"
    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None

# =========================
# REQUIREMENTS EXTRACTION
# =========================

def extract_phone(text):

    pattern = r'(\+?\d[\d\s-]{8,}\d)'

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None

# =========================
# REQUIREMENTS EXTRACTION
# =========================

def extract_requirements(text):

    requirement_keywords = [
        "crm",
        "automation",
        "integration",
        "pricing",
        "dashboard",
        "analytics",
        "ai",
        "software",
        "service",
        "platform"
    ]

    text_lower = text.lower()

    for keyword in requirement_keywords:

        if keyword in text_lower:
            return text

    return None

# =========================
# LEAD CLASSIFICATION
# =========================

def classify_lead(text):

    text = text.lower()

    hot_keywords = [
        "pricing",
        "demo",
        "buy",
        "crm",
        "automation",
        "subscription"
    ]

    warm_keywords = [
        "interested",
        "looking",
        "exploring"
    ]

    for keyword in hot_keywords:
        if keyword in text:
            return "hot"

    for keyword in warm_keywords:
        if keyword in text:
            return "warm"

    return "cold"


# =========================
# EXTRACT LEAD INFO
# =========================

def extract_lead_info(text):

    lead_data = {
        "name": extract_name(text),
        "company": extract_company(text),
        "email": extract_email(text),
        "phone":extract_phone(text),
        "requirements": extract_requirements(text),
        "classification": classify_lead(text),
        "created_at": datetime.now(UTC)
    }

    return lead_data

# =========================
# MISSING FIELDS
# =========================
def get_missing_fields(state):

    missing = []

    if not state["name"]:
        missing.append("name")

    if not state["email"]:
        missing.append("email")

    if not state["company"]:
        missing.append("company name")

    if not state["requirements"]:
        missing.append("requirements")
    return missing

# =========================
# SAVE LEAD
# =========================

async def save_lead(lead_data):

    await lead_collection.insert_one(lead_data)

    return {
        "message": "Lead saved successfully"
    }