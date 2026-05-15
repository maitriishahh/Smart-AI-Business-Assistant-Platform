from backend.app.memory.conversation_history import get_recent_conversations

async def build_short_term_context(user_id:str):
    conversations = await get_recent_conversations(user_id)

    context = ""
    for convo in conversations:
        context +=f"""
User:{convo['user_msg']}
Assistant:{convo['assistant_response']}"""
        return context.strip()