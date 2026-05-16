from backend.app.agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

async def ask_question(message: str, session_id: str, user_id:str):
    result = await orchestrator.run(message=message,
        session_id=session_id,
        user_id=user_id
    )

    return result