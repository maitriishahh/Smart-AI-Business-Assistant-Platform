from datetime import datetime, UTC

from backend.app.memory.lead_state import (
    get_lead_state
)

from backend.app.services.lead_service import (
    extract_email,
    extract_name,
    extract_company,
    extract_phone,
    extract_requirements,
    classify_lead,
    get_missing_fields,
    save_lead
)

from backend.app.automations.followup_generator import (
    generate_followup
)


async def lead_capture_pipeline(
    message: str,
    session_id: str
):

    state = get_lead_state(session_id)

    # =========================================
    # PHONE STEP
    # =========================================

    if state["awaiting_phone"]:

        if message.lower().strip() != "skip":

            extracted_phone = extract_phone(message)

            if extracted_phone:
                state["phone"] = extracted_phone

        lead_data = {
            "name": state["name"],
            "email": state["email"],
            "phone": state["phone"],
            "company": state["company"],
            "requirements": state["requirements"],
            "classification": classify_lead(
                state["requirements"]
            ),
            "created_at": datetime.now(UTC)
        }

        await save_lead(lead_data)

        # =========================================
        # FIXED ASYNC BUG
        # =========================================

        followup_result = await generate_followup(
            lead_data
        )

        followup_message = followup_result.get(
            "followup_email",
            "Follow-up could not be generated."
        )

        # =========================================
        # RESET STATE
        # =========================================

        state["collecting"] = False
        state["awaiting_phone"] = False
        state["name"] = None
        state["email"] = None
        state["phone"] = None
        state["company"] = None
        state["requirements"] = None

        return {
            "completed": True,
            "reply": f"""
Thank you! Your lead has been captured successfully.

AI-Generated Follow-Up Message:

{followup_message}
""".strip(),
            "lead_data": lead_data
        }

    # =========================================
    # NORMAL EXTRACTION
    # =========================================

    extracted_name = extract_name(message)
    extracted_email = extract_email(message)
    extracted_company = extract_company(message)
    extracted_phone = extract_phone(message)
    extracted_requirements = extract_requirements(message)

    if extracted_name:
        state["name"] = extracted_name

    if extracted_email:
        state["email"] = extracted_email

    if extracted_company:
        state["company"] = extracted_company

    if extracted_phone:
        state["phone"] = extracted_phone

    if extracted_requirements:
        state["requirements"] = extracted_requirements

    # =========================================
    # CHECK MISSING FIELDS
    # =========================================

    missing_fields = get_missing_fields(state)

    if missing_fields:

        state["collecting"] = True

        missing_text = ", ".join(missing_fields)

        return {
            "completed": False,
            "reply": f"Please provide your {missing_text}."
        }

    # =========================================
    # ASK OPTIONAL PHONE
    # =========================================

    if not state["phone"]:

        state["awaiting_phone"] = True

        return {
            "completed": False,
            "reply": """
Would you also like to share your phone number for easier contact?

If yes, please provide it.
Otherwise, type 'skip'.
"""
        }

    # =========================================
    # SAVE LEAD
    # =========================================

    lead_data = {
        "name": state["name"],
        "email": state["email"],
        "phone": state["phone"],
        "company": state["company"],
        "requirements": state["requirements"],
        "classification": classify_lead(
            state["requirements"]
        ),
        "created_at": datetime.now(UTC)
    }

    await save_lead(lead_data)

    # =========================================
    # FIXED ASYNC BUG
    # =========================================

    followup_result = await generate_followup(
        lead_data
    )

    followup_message = followup_result.get(
        "followup_email",
        "Follow-up could not be generated."
    )

    # =========================================
    # RESET STATE
    # =========================================

    state["collecting"] = False
    state["awaiting_phone"] = False
    state["name"] = None
    state["email"] = None
    state["phone"] = None
    state["company"] = None
    state["requirements"] = None

    return {
        "completed": True,
        "reply": f"""
Thank you! Your lead has been captured successfully.

AI-Generated Follow-Up Message:

{followup_message}
""".strip(),
        "lead_data": lead_data
    }