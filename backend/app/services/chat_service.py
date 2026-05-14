from google import genai
from backend.app.config.settings import settings
from backend.app.rag.retriever import retrieve_relevant_chunks

client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def ask_question(question:str, user_id:str):
    chunks = await retrieve_relevant_chunks(question=question,user_id=user_id)

    context = "\n\n".join(chunks)
    prompt = f"""
You are an AI business assistant. Answer ONLY usig the provided context.If the answer is not found,
say:
"I could not find that information in the uploaded documents."

CONTEXT:
{context}

QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text