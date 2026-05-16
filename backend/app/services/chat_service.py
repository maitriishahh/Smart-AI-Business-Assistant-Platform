from backend.app.agents.workflow_graph import workflow

from backend.app.services.lead_service import (
    detect_lead_intent
)

from backend.app.workflows.lead_workflow import (
    lead_capture_pipeline
)

from backend.app.memory.lead_state import (
    get_lead_state
)

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

async def ask_question(
    message: str,
    session_id: str,
    user_id: str
):

    if is_greeting(message):

        return {
        "response": "Hello! How can I help you today?"
    }

    state = get_lead_state(session_id)

    # Continue collecting lead info
    if state["collecting"]:

        lead_response = await lead_capture_pipeline(
            message,
            session_id
        )

        return {
            "response": lead_response["reply"]
        }

    # Detect high intent
    if detect_lead_intent(message) and not state["collecting"]:

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

    # Normal AI Workflow
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