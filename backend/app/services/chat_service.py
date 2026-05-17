from backend.app.agents.workflow_graph import workflow

from backend.app.workflows.lead_workflow import (
    lead_capture_pipeline
)

from backend.app.memory.lead_state import (
    get_lead_state
)

from backend.app.rag.retriever import (
    retrieve_relevant_chunks
)

from backend.app.memory.short_term import (
    build_short_term_context
)

from backend.app.memory.long_term import (
    build_long_term_context
)

from backend.app.memory.conversation_history import (
    save_convo
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



    # =========================================
    # LEAD STATE
    # =========================================

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
    # MEMORY CONTEXT
    # =========================================

    short_term_context = await build_short_term_context(
        user_id
    )

    long_term_context = await build_long_term_context(
        user_id
    )



    # =========================================
    # RAG RETRIEVAL
    # =========================================

    retrieved_docs = await retrieve_relevant_chunks(
        question=message,
        user_id=user_id
    )


 # =========================================
    # STRONG LEAD INTENT
    # =========================================

    strong_lead_keywords = [

    "hire",
    "hiring",
    "book a consultation",
    "book consultation",
    "book a call",
    "schedule a call",
    "schedule a meeting",
    "contact me",
    "i want your service",
    "interested in your service",
    "work with you",
    "consultation",
    "demo",
    "my email is",
    "my company is",
]

    message_lower = message.lower()

    if (
    any(
        keyword in message_lower
        for keyword in strong_lead_keywords
    )
    and not state["collecting"]
):

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
    # RAG + AI WORKFLOW
    # =========================================

    if retrieved_docs and len(retrieved_docs) > 0:

        print(
            "RAG documents found → routing to AI workflow"
        )

        result = await workflow.ainvoke({

            "message": message,

            "session_id": session_id,

            "user_id": user_id,

            "short_term_context":
                short_term_context,

            "long_term_context":
                long_term_context
        })



        # =========================================
        # SAVE CONVERSATION
        # =========================================

        await save_convo(

            user_id=user_id,

            session_id=session_id,

            user_msg=message,

            assistant_response=result["response"]
        )



        return {

            "plan": result["plan"],

            "response": result["response"],

            "validation": result["validation"],

            "provider": result["provider"]
        }



    # =========================================
    # NORMAL AI CHAT
    # =========================================

    result = await workflow.ainvoke({

        "message": message,

        "session_id": session_id,

        "user_id": user_id,

        "short_term_context":
            short_term_context,

        "long_term_context":
            long_term_context
    })



    # =========================================
    # SAVE CONVERSATION
    # =========================================

    await save_convo(

        user_id=user_id,

        session_id=session_id,

        user_msg=message,

        assistant_response=result["response"]
    )



    # =========================================
    # RETURN RESPONSE
    # =========================================

    return {

        "plan": result["plan"],

        "response": result["response"],

        "validation": result["validation"],

        "provider": result["provider"]
    }