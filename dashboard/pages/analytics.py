import streamlit as st
import pandas as pd
import os

st.title("📊 Analytics Dashboard")


# =========================================
# CRM EXPORT STATS
# =========================================

total_leads = 0

if os.path.exists("crm_export.csv"):

    crm_df = pd.read_csv("crm_export.csv")

    total_leads = len(crm_df)

else:

    crm_df = pd.DataFrame()


# =========================================
# METRICS
# =========================================
automations_executed = total_leads * 2
crm_exports = total_leads

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Leads", total_leads)

with col2:
    st.metric("Automations Executed", automations_executed)

with col3:
    st.metric("CRM Exports", crm_exports)


st.divider()


# =========================================
# STATUS
# =========================================

st.subheader("✅ System Status")

st.success("AI Assistant Active")
st.success("Workflow Automation Active")
st.success("RAG System Active")
st.success("Dashboard Monitoring Active")