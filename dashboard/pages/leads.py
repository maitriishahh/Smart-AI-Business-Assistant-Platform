import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


import streamlit as st
from pymongo import MongoClient

from backend.app.config.settings import settings


# =========================================
# MONGODB CONNECTION
# =========================================

client = MongoClient(settings.MONGODB_URL)

db = client[settings.DATABASE_NAME]

leads_collection = db["leads"]


# =========================================
# PAGE TITLE
# =========================================

st.title("📋 Leads Dashboard")


# =========================================
# FETCH LEADS
# =========================================

all_leads = list(leads_collection.find())


# =========================================
# LEAD METRICS
# =========================================

total_leads = len(all_leads)

hot_leads = len([
    lead for lead in all_leads
    if lead.get("classification") == "hot"
])

warm_leads = len([
    lead for lead in all_leads
    if lead.get("classification") == "warm"
])

cold_leads = len([
    lead for lead in all_leads
    if lead.get("classification") == "cold"
])


# =========================================
# METRIC CARDS
# =========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Leads", total_leads)

with col2:
    st.metric("🔥 Hot Leads", hot_leads)

with col3:
    st.metric("🌤 Warm Leads", warm_leads)

with col4:
    st.metric("❄️ Cold Leads", cold_leads)


st.divider()


# =========================================
# EMPTY STATE
# =========================================

if not all_leads:

    st.info("No leads captured yet.")


# =========================================
# LEAD RECORDS
# =========================================

for lead in all_leads:

    st.subheader(lead.get("name", "Unknown Lead"))

    st.write("🏢 Company:", lead.get("company"))

    st.write("📧 Email:", lead.get("email"))

    st.write("📱 Phone:", lead.get("phone"))

    st.write(
        "🎯 Classification:",
        lead.get("classification")
    )

    st.write(
        "📝 Requirements:",
        lead.get("requirements")
    )

    st.write(
        "🕒 Created At:",
        lead.get("created_at")
    )

    st.divider()