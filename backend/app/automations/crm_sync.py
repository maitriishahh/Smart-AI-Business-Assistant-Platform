import csv
from datetime import datetime, UTC


async def sync_lead_to_crm(lead_data: dict):

    file_path = "crm_export.csv"

    file_exists = False

    try:
        with open(file_path, "r"):
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        # Write header only once
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

    return {
        "status": "success",
        "message": "Lead synced to CRM export successfully"
    }