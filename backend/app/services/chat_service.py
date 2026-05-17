from backend.app.agents.workflow_graph import workflow

# from backend.app.services.lead_service import (
#     detect_lead_intent
# )

from backend.app.workflows.lead_workflow import (
    lead_capture_pipeline
)

from backend.app.memory.lead_state import (
    get_lead_state
)

from backend.app.rag.retriever import (
    retrieve_relevant_chunks
)


# =========================================
# GREETING DETECTION
# =========================================

def is_greeting(message: str):

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening",
        "good afternoon"
    ]

    return message.lower().strip() in greetings


# =========================================
# MAIN CHAT SERVICE
# =========================================

async def ask_question(
    message: str,
    session_id: str,
    user_id: str
):

    # =========================================
    # GREETING
    # =========================================

    if is_greeting(message):

        return {
            "response": "Hello! How can I help you today?"
        }

    state = get_lead_state(session_id)

    # =========================================
    # CONTINUE LEAD COLLECTION
    # =========================================

    if state["collecting"]:

        lead_response = await lead_capture_pipeline(
            message,
            session_id
        )

        return {
            "response": lead_response["reply"]
        }

    # =========================================
    # PRIORITY 1 → STRONG LEAD INTENT
    # =========================================

    strong_lead_keywords = [
        "hire",
        "hiring",
        "book a consultation",
        "book consultation",
        "book a call",
        "schedule a call",
        "contact me",
        "i want your service",
        "interested in your service",
        "work with you",
        "consultation",
        "my email is",
        "my company is",
    ]

    message_lower = message.lower()

    if any(keyword in message_lower for keyword in strong_lead_keywords):

        state["collecting"] = True

        return {
            "response": """
    I'd be happy to help.

    Please provide your:
    - Name
    - Email
    - Company Name
    - Requirements

    (Optional: Phone Number)
    """
        }


    # =========================================
    # PRIORITY 2 → RAG RETRIEVAL
    # =========================================

    retrieved_docs = await retrieve_relevant_chunks(
        question=message,
        user_id=user_id
    )

    if retrieved_docs and len(retrieved_docs) > 0:

        print("RAG documents found → routing to AI workflow")

        result = await workflow.ainvoke({
            "message": message,
            "session_id": session_id,
            "user_id": user_id
        })

        return {
            "plan": result["plan"],
            "response": result["response"],
            "validation": result["validation"],
            "provider": result["provider"]
        }

    # =========================================
    # PRIORITY 3 → NORMAL AI CHAT
    # =========================================

    result = await workflow.ainvoke({
        "message": message,
        "session_id": session_id,
        "user_id": user_id
    })

    return {
        "plan": result["plan"],
        "response": result["response"],
        "validation": result["validation"],
        "provider": result["provider"]
    }