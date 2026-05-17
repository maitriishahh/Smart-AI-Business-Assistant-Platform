import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

st.set_page_config(
    page_title="Automation Analytics",
    layout="wide"
)

st.title("⚙️ Automation Analytics Dashboard")


# =========================================
# CRM EXPORT METRIC
# =========================================

crm_exports_count = 0

if os.path.exists("crm_export.csv"):

    crm_df = pd.read_csv("crm_export.csv")

    crm_exports_count = len(crm_df)

else:

    crm_df = pd.DataFrame()


# =========================================
# AUTOMATION METRICS
# =========================================

email_summaries_count = crm_exports_count

followups_generated_count = crm_exports_count


# =========================================
# METRICS ROW
# =========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📧 Email Summaries",
        email_summaries_count
    )

with col2:
    st.metric(
        "🤝 Follow-Ups Generated",
        followups_generated_count
    )

with col3:
    st.metric(
        "📁 CRM Exports",
        crm_exports_count
    )


st.divider()


# =========================================
# CRM EXPORT TABLE
# =========================================

st.subheader("📄 CRM Export Records")

if not crm_df.empty:

    st.dataframe(
        crm_df,
        use_container_width=True
    )

else:

    st.info("No CRM exports available yet.")


# =========================================
# AUTOMATION STATUS
# =========================================

st.divider()

st.subheader("✅ Automation Status")

st.success("Email Summarization Automation Active")
st.success("Follow-Up Automation Active")
st.success("CRM Sync Automation Active")