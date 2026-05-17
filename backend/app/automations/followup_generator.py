from google import genai
from groq import Groq

from backend.app.config.settings import settings


gemini_client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

groq_client = Groq(
    api_key=settings.GROQ_API_KEY
)


async def generate_followup(
    lead_data,
    followup_type="general"
):

    prompt = f"""
Generate a professional business follow-up email.

Follow-Up Type:
{followup_type}

Lead Details:
Name: {lead_data.get("name")}
Company: {lead_data.get("company")}
Requirements: {lead_data.get("requirements")}
Lead Classification: {lead_data.get("classification")}

Keep the email:
- concise
- professional
- friendly
- business-oriented

End the email with:
Best regards,
AI Business Assistant Team
"""

    # =========================
    # GEMINI PRIMARY
    # =========================

    try:

        print("Generating follow-up using Gemini...")

        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "status": "success",
            "provider": "Gemini",
            "followup_email": response.text
        }

    # =========================
    # GROQ FALLBACK
    # =========================

    except Exception as e:

        print("Gemini follow-up generation failed:", e)

        print("Switching to Groq...")

        groq_response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "status": "success",
            "provider": "Groq",
            "followup_email": (
                groq_response
                .choices[0]
                .message.content
            )
        }