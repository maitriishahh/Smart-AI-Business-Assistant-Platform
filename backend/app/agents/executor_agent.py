from backend.app.rag.retriever import retrieve_relevant_chunks
from backend.app.config.settings import settings
from backend.app.workflows.chat_workflow import (
    get_convo_context,
    update_convo_context
)
from google import genai
from groq import Groq


class ExecutorAgent:

    def __init__(self):

        # =========================
        # GEMINI CLIENT
        # =========================
        self.gemini_client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        # =========================
        # GROQ CLIENT
        # =========================
        self.groq_client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    async def execute(
        self,
        message: str,
        session_id: str,
        user_id: str,
        plan: dict
    ):

        # =========================
        # LOAD MEMORY
        # =========================
        history = await get_convo_context(user_id)

        # LIMIT HISTORY
        history = history[-3:]

        formatted_history = ""

        for chat in history:

            formatted_history += (
                f"User: {chat['user']}\n"
                f"Assistant: {chat['assistant']}\n\n"
            )

        # =========================
        # RETRIEVE DOCUMENTS
        # =========================
        retrieved_docs = []
        if plan["needs_retrieval"]:

            prompt = f"""
You are an AI business assistant.

RULES:
- Use uploaded document context when relevant.
- Use conversation history for continuity.
- Be concise and professional.
- Avoid hallucinations or invented information.
- Answer ONLY using uploaded document context.
- Do NOT use outside knowledge.
- If information is unavailable, say:
"I could not find that information in the uploaded documents."

Conversation:
{formatted_history}

Document Context:
{context}

User Message:
{message}
"""

        else:

            prompt = f"""
You are an AI business assistant.

RULES:
- Use conversation history for continuity.
- Be concise and professional.
- Avoid hallucinations or invented information.
- If no relevant document context exists, you may answer using general knowledge.
- If you genuinely do not know the answer, say:
"I could not find that information."

Conversation:
{formatted_history}

User Message:
{message}
"""
            retrieved_docs = await retrieve_relevant_chunks(
            question=message,
            user_id=user_id
        )

            # LIMIT CHUNKS
            retrieved_docs = retrieved_docs[:2]

        # =========================
        # BUILD CONTEXT
        # =========================
        context = (
            "\n\n".join(retrieved_docs)
            if retrieved_docs
            else "No relevant uploaded document context available."
        )

    
        # =========================
        # GEMINI PRIMARY
        # =========================
        try:

            print("Using Gemini...")

            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            assistant_reply = response.text

            provider = "gemini"

        # =========================
        # GROQ FALLBACK
        # =========================
        except Exception as e:

            print("Gemini failed:", e)

            print("Switching to Groq...")

            groq_response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            assistant_reply = (
                groq_response
                .choices[0]
                .message.content
            )

            provider = "groq"

        # =========================
        # UPDATE MEMORY
        # =========================
        await update_convo_context(
            user_id=user_id,
            session_id=session_id,
            user_msg=message,
            assistant_response=assistant_reply
        )

        # =========================
        # RETURN RESPONSE
        # =========================
        return {
            "response": assistant_reply,
            "retrieved_docs": retrieved_docs,
            "provider": provider
        }