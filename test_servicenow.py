import os
import requests
from dotenv import load_dotenv

load_dotenv()

instance = os.getenv("SERVICENOW_INSTANCE")
username = os.getenv("SERVICENOW_USERNAME")
password = os.getenv("SERVICENOW_PASSWORD")

url = f"{instance}/api/now/table/incident"

data = {
    "short_description": "VPN not connecting",
    "description": "Created from Agentic AI Service Desk",
    "category": "network",
    "impact": "2",
    "urgency": "2"
}

response = requests.post(
    url,
    auth=(username, password),
    headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
    },
    json=data,
    timeout=30
)

print("Status Code:", response.status_code)
print("\nResponse:")
print(response.text)