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

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "short_description": short_description,
        "description": description,
        "category": category.lower(),
        "priority": priority,
        "assignment_group": assignment_group
    }

    response = requests.post(
        url,
        auth=(USERNAME, PASSWORD),
        headers=headers,
        json=payload
    )

    return response