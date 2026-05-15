from google import genai
from backend.app.config.settings import settings
from backend.app.rag.retriever import retrieve_relevant_chunks
from backend.app.workflows.chat_workflow import(get_convo_context, update_convo_context)

client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def ask_question(message:str, session_id: str, user_id:str):
    chunks = await retrieve_relevant_chunks(question=message,user_id=user_id)
    
    # if not chunks:
    #     return {
    #         "response": (
    #             "I could not find relevant "
    #             "information in the uploaded documents."
    #         ),
    #         "session_id": session_id,
    #         "sources_used": False
    #     }
    
    context = ("\n\n".join(chunks)
        if chunks
        else "No relevant uploaded document context available.")

    history = await get_convo_context(user_id)
    formatted_history = ""
    for chat in history:
        formatted_history += (
            f"User: {chat['user']}\n"
            f"Assistant: {chat['assistant']}\n\n"
        )
    prompt = f"""
You are an intelligent AI business assistant.

STRICT RULES:
- Prioritize uploaded document context when available.
- Use previous conversation history for conversational continuity.
- If the answer is unavailable in uploaded documents but exists in previous conversation history, use the conversation history.
- Maintain professional business tone.
- Avoid slang or overly casual wording.
- Keep responses concise and factual.
- If information is unavailable in both uploaded documents and conversation history, clearly say so.
- If answer not found, say:
"I could not find that information in the uploaded documents."

PREVIOUS CONVERSATION:
{formatted_history}

DOCUMENT CONTEXT:
{context}

CURRENT USER MESSAGE:
{message}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    assistant_reply = response.text
    
    await update_convo_context(user_id=user_id,session_id=session_id, user_msg = message, assistant_response=assistant_reply)
    
    return {
        "response":assistant_reply,
        "session_id":session_id,
        "sources_used":True
    }