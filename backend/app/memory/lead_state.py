lead_sessions = {}


def get_lead_state(session_id):

    if session_id not in lead_sessions:

        lead_sessions[session_id] = {
            "collecting": False,
            "awaiting_phone": False,
            "name": None,
            "email": None,
            "phone":None,
            "company": None,
            "requirements": None
        }

    return lead_sessions[session_id]