import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


import streamlit as st
from pymongo import MongoClient
from backend.app.config.settings import settings

client = MongoClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]
leads = db["leads"]
st.title("Leads Dashboard")

all_leads = list(leads.find())

for lead in all_leads:
    st.subheader(lead.get('name'))
    
    st.write("Company:", lead.get("company"))
    st.write("Email:", lead.get("email"))
    st.write("Phone:",lead.get("phone"))
    st.write("Classification:", lead.get("classification"))
    st.write("Requirements:", lead.get("requirements"))
    st.write("Created At:", lead.get("created_at"))
    st.divider()

