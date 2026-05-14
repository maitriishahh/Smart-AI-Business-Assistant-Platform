session_store = {}

def get_convo_context(session_id:str):
    return session_store.get(session_id,[])

def update_convo_context(session_id:str, user_msg: str, assistant_response:str):
    if session_id not in session_store:
        session_store[session_id]=[]
    session_store[session_id].append({
        "user":user_msg,
        "assistant": assistant_response
    })

    session_store[session_id]=(
        session_store[session_id][-5:]
    )