import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Business Assistant",
    layout="wide"
)

st.title("AI Business Assistant")

# SESSION STATE

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR

with st.sidebar:

    st.header("Configuration")

    jwt_token = st.text_input(
        "JWT Token",
        type="password"
    )

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if st.button("Upload PDF"):

        if uploaded_file and jwt_token:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            headers = {
                "Authorization": f"Bearer {jwt_token}"
            }

            response = requests.post(
                f"{API_URL}/upload/pdf",
                files=files,
                headers=headers
            )

            if response.status_code == 200:
                st.success("PDF uploaded successfully")

            else:
                st.error(response.text)

        else:
            st.warning("Upload PDF and JWT token required")

# CHAT HISTORY DISPLAY

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# USER INPUT

prompt = st.chat_input("Ask a question")

# SEND MESSAGE

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    payload = {
        "message": prompt,
        "session_id": st.session_state.session_id
    }

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = requests.post(
                f"{API_URL}/chat/query",
                json=payload,
                headers=headers
            )

            if response.status_code == 200:

                data = response.json()

                assistant_reply = data["response"]

            else:

                assistant_reply = "Error generating response"

            st.markdown(assistant_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })