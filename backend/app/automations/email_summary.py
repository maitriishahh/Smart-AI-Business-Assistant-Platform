from google import genai
from groq import Groq
import json
from backend.app.config.settings import settings

gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)

groq_client = Groq(api_key=settings.GROQ_API_KEY)

async def summarize_email(email_content:str):
    prompt = f"""
    You are an AI business assistant.

    Analyze the following email and return:

    1. Short summary
    2. Urgency level (low, medium, high)
    3. Action items as a list
    4. Professional suggested reply

    Always end the suggested reply with:

    Best regards,
    AI Business Assistant Team
    Return ONLY valid JSON.

    Format:
    {{
        "summary": "...",
        "urgency": "...",
        "action_items": ["...", "..."],
        "suggested_reply": "..."
    }}

    Email:
    {email_content}
    """
    try:

        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text_response = response.text.strip()

        # Remove markdown if present
        text_response = text_response.replace("```json", "").replace("```", "").strip()
        print("Groq Response:")
        print(text_response)
        return json.loads(text_response)

    except Exception as gemini_error:

        print(f"Gemini failed: {gemini_error}")

        # =========================
        # GROQ FALLBACK
        # =========================
        try:

            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )

            text_response = completion.choices[0].message.content.strip()

            text_response = text_response.replace("```json", "").replace("```", "").strip()
            print("Groq Response:")
            print(text_response)
            return json.loads(text_response)

        except Exception as groq_error:

            print(f"Groq failed: {groq_error}")

            return {
                "summary": "Unable to summarize email",
                "urgency": "unknown",
                "action_items": [],
                "suggested_reply": "Unable to generate reply"
            }