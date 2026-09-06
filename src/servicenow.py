import logging
import os

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)
load_dotenv()

INSTANCE = os.getenv("SERVICENOW_INSTANCE")
USERNAME = os.getenv("SERVICENOW_USERNAME")
PASSWORD = os.getenv("SERVICENOW_PASSWORD")

_session = None


def _get_session():
    global _session
    if _session is None:
        session = requests.Session()
        retries = Retry(
            total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504]
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))
        _session = session
    return _session


def create_incident(
    short_description, description, category, priority, assignment_group
):
    """Create an incident in ServiceNow.

    Returns dict: {success: bool, number, sys_id, status_code?, message}
    """
    if not (INSTANCE and USERNAME and PASSWORD):
        msg = "ServiceNow credentials are not configured. Set SERVICENOW_INSTANCE, SERVICENOW_USERNAME, and SERVICENOW_PASSWORD in .env or environment."
        logger.error(msg)
        return {"success": False, "message": msg}

    url = f"{INSTANCE.rstrip('/')}/api/now/table/incident"

    data = {
        "short_description": short_description,
        "description": description,
        "category": category,
        "priority": priority,
    }

    if assignment_group:
        data["assignment_group"] = assignment_group

    session = _get_session()

    try:
        response = session.post(
            url,
            auth=(USERNAME, PASSWORD),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json=data,
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.exception("Failed to create ServiceNow incident")
        return {"success": False, "message": str(exc)}

    if response.status_code == 201:
        result = response.json().get("result", {})
        return {
            "success": True,
            "number": result.get("number"),
            "sys_id": result.get("sys_id"),
            "message": "ServiceNow incident created successfully",
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "message": response.text,
    }
