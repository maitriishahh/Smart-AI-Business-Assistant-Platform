from backend.app.automations.email_summary import summarize_email
from backend.app.automations.crm_sync import sync_lead_to_crm
from backend.app.automations.followup_generator import generate_followup


# =========================================
# EMAIL SUMMARIZATION WORKFLOW
# =========================================

async def run_email_summarization_workflow(
    email_content: str
):

    print("Running email summarization workflow...")

    result = await summarize_email(
        email_content
    )

    return result


# =========================================
# CRM SYNC WORKFLOW
# =========================================

async def run_crm_sync_workflow(
    lead_data: dict
):

    print("Running CRM sync workflow...")

    result = await sync_lead_to_crm(
        lead_data
    )

    return result


# =========================================
# FOLLOW-UP WORKFLOW
# =========================================

async def run_followup_workflow(
    lead_data: dict,
    followup_type: str = "general"
):

    print("Running follow-up workflow...")

    result = await generate_followup(
        lead_data,
        followup_type
    )

    return result


# =========================================
# COMPLETE LEAD AUTOMATION WORKFLOW
# =========================================

async def handle_new_lead_workflow(
    lead_data: dict,
    followup_type: str = "general"
):

    print("Starting complete lead automation workflow...")

    # STEP 1 → CRM Sync
    crm_result = await sync_lead_to_crm(
        lead_data
    )

    # STEP 2 → Follow-Up Generation
    followup_result = await generate_followup(
        lead_data,
        followup_type
    )

    return {
        "workflow_status": "success",
        "crm_sync": crm_result,
        "followup": followup_result
    }