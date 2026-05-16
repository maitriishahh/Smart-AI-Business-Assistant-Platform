from google import genai

from backend.app.config.settings import settings


client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_followup(lead_data):

    prompt = f"""
    Generate a professional follow-up email.

    Lead Details:
    {lead_data}

    Keep it concise and professional.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text