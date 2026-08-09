import os
import requests
from dotenv import load_dotenv

load_dotenv()

INSTANCE = os.getenv("SERVICENOW_INSTANCE")
USERNAME = os.getenv("SERVICENOW_USERNAME")
PASSWORD = os.getenv("SERVICENOW_PASSWORD")


def create_incident(
    short_description,
    description,
    category,
    priority,
    assignment_group
):

    url = f"{INSTANCE}/api/now/table/incident"

    data = {
        "short_description": short_description,
        "description": description,
        "category": category,
        "priority": priority
    }

    if assignment_group:
        data["assignment_group"] = assignment_group

    response = requests.post(
        url,
        auth=(USERNAME, PASSWORD),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json=data,
        timeout=30
    )

    if response.status_code == 201:
        result = response.json()["result"]

        return {
            "success": True,
            "number": result.get("number"),
            "sys_id": result.get("sys_id"),
            "message": "ServiceNow incident created successfully"
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "message": response.text
    }