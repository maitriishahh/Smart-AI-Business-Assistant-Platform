import streamlit as st
import pandas as pd
from pymongo import MongoClient
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)
from backend.app.config.settings import settings


st.title("💬 Chat Logs")

# =========================================
# MONGODB CONNECTION
# =========================================

client = MongoClient(settings.MONGODB_URL)

db = client[settings.DATABASE_NAME]

chat_collection = db["conversations"]


# =========================================
# FETCH CHAT LOGS
# =========================================

chat_logs = list(
    chat_collection
    .find()
    .sort("timestamp", -1)
    .limit(20)
)


# =========================================
# FORMAT DATA
# =========================================

formatted_logs = []

for chat in chat_logs:

    formatted_logs.append({
        "User": chat.get("user_name", "Unknown"),
        "Query": chat.get("user_message", ""),
        "AI Response": chat.get("assistant_response", ""),
        "Timestamp": str(chat.get("timestamp", ""))
    })


df = pd.DataFrame(formatted_logs)


# =========================================
# DISPLAY
# =========================================

if not df.empty:

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info("No chat logs available.")