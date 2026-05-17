import csv
from datetime import datetime, UTC

from backend.app.database.mongodb import database

db = database


async def sync_lead_to_crm(lead_data: dict):

    # =========================================
    # CSV EXPORT
    # =========================================

    file_path = "crm_export.csv"

    file_exists = False

    try:

        with open(file_path, "r"):

            file_exists = True

    except FileNotFoundError:

        file_exists = False



    with open(
        file_path,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # Write Header Once
        if not file_exists:

            writer.writerow([
                "name",
                "email",
                "company",
                "phone",
                "requirements",
                "priority",
                "timestamp"
            ])



        writer.writerow([

            lead_data.get("name"),

            lead_data.get("email"),

            lead_data.get("company"),

            lead_data.get("phone"),

            lead_data.get("requirements"),

            lead_data.get("priority"),

            datetime.now(UTC).isoformat()
        ])



    # =========================================
    # SAVE TO MONGODB
    # =========================================

    await db["leads"].insert_one({

        "name":
            lead_data.get("name"),

        "email":
            lead_data.get("email"),

        "company":
            lead_data.get("company"),

        "phone":
            lead_data.get("phone"),

        "requirements":
            lead_data.get("requirements"),

        "classification":
            lead_data.get("priority"),

        "created_at":
            datetime.now(UTC)
    })



    # =========================================
    # RETURN
    # =========================================

    return {

        "status": "success",

        "message":
            "Lead synced to CRM successfully"
    }