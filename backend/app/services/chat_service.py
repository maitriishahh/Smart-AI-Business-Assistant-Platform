from backend.app.agents.workflow_graph import workflow


async def ask_question(
    message: str,
    session_id: str,
    user_id: str
):

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