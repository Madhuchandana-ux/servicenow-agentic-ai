"""
===========================================================
AI Service Desk Automation Dataset Generator
Author: Madhu Chandana
Description:
Generates enterprise-grade synthetic datasets for:
1. Users
2. Assets
3. Engineers
4. Incidents
5. Knowledge Base

This dataset is designed for:
- Machine Learning
- Agentic AI
- RAG
- ServiceNow Integration
===========================================================
"""

# ============================
# IMPORTS
# ============================

import os
import random
import logging
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

# ============================
# RANDOM SEED
# ============================

random.seed(42)
np.random.seed(42)
fake = Faker()
Faker.seed(42)

# ============================
# CREATE DATA FOLDER
# ============================

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# ============================
# LOGGING
# ============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

logger.info("Dataset Generator Started")

# ============================
# CONFIGURATION
# ============================

NUM_USERS = 1000
NUM_ASSETS = 2000
NUM_ENGINEERS = 20
NUM_INCIDENTS = 10000

COMPANY_NAME = "ABC Technologies"

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)

# ============================
# MASTER DATA
# ============================

DEPARTMENTS = [
    "Finance",
    "Human Resources",
    "Sales",
    "Marketing",
    "Operations",
    "IT",
    "Customer Support",
    "Legal",
    "Procurement",
    "Administration"
]

LOCATIONS = [
    "Hyderabad",
    "Bangalore",
    "Chennai",
    "Mumbai",
    "Delhi",
    "Pune",
    "Kolkata",
    "Noida"
]

DEVICE_TYPES = [
    "Laptop",
    "Desktop",
    "Printer",
    "Server",
    "Mobile",
    "Tablet"
]

STATUS = [
    "Open",
    "In Progress",
    "Resolved",
    "Closed"
]

IMPACT = [
    "Low",
    "Medium",
    "High"
]

URGENCY = [
    "Low",
    "Medium",
    "High"
]
CATEGORIES = {

    "Hardware": [
        "Laptop not booting",
        "Keyboard not working",
        "Battery not charging",
        "Monitor flickering",
        "Mouse disconnected",
        "USB ports not working",
        "Hard disk failure",
        "Laptop overheating"
    ],

    "Software": [
        "MS Office not opening",
        "Chrome crashing",
        "Excel freezing",
        "Adobe Acrobat not responding",
        "Application installation failed",
        "Teams crashing",
        "Zoom not opening",
        "Software update failed"
    ],

    "Network": [
        "VPN not connecting",
        "Internet slow",
        "WiFi disconnected",
        "Server unreachable",
        "Cannot access shared drive",
        "DNS resolution failed",
        "Network timeout",
        "LAN cable unplugged"
    ],

    "Email": [
        "Outlook not opening",
        "Mailbox full",
        "Email sync issue",
        "Cannot send email",
        "Exchange server unavailable",
        "Spam emails received",
        "Calendar not syncing",
        "Attachment missing"
    ],

    "Security": [
        "Phishing email",
        "Malware detected",
        "Unauthorized login",
        "Firewall blocked access",
        "Password compromised",
        "Account locked",
        "Suspicious attachment",
        "Ransomware alert"
    ],

    "Printer": [
        "Printer offline",
        "Printer paper jam",
        "Printer toner low",
        "Unable to print",
        "Printer queue stuck",
        "Printer driver missing",
        "Scanner not working",
        "Network printer unavailable"
    ],

    "Database": [
        "Database connection failed",
        "SQL timeout",
        "Database server down",
        "Backup failed",
        "Replication error",
        "Database locked",
        "Deadlock detected",
        "Slow query execution"
    ],

    "Cloud": [
        "AWS EC2 stopped",
        "Azure VM unavailable",
        "Cloud API timeout",
        "Storage inaccessible",
        "Cloud deployment failed",
        "Lambda function error",
        "Load balancer unhealthy",
        "S3 permission denied"
    ],

    "Account": [
        "Cannot login",
        "Password reset",
        "Permission denied",
        "Account locked",
        "New user creation",
        "Access request pending",
        "User profile missing",
        "MFA issue"
    ],

    "Mobile": [
        "Company phone not syncing",
        "Tablet frozen",
        "Battery draining quickly",
        "Device enrollment failed",
        "Mobile VPN issue",
        "SIM activation failed",
        "Mobile app crashing",
        "Mobile email issue"
    ]
}
ASSIGNMENT_GROUPS = {

    "Hardware":"Desktop Support",

    "Software":"Application Support",

    "Network":"Network Team",

    "Email":"Messaging Team",

    "Security":"Security Operations",

    "Printer":"Printer Support",

    "Database":"Database Team",

    "Cloud":"Cloud Operations",

    "Account":"Identity Management",

    "Mobile":"Mobility Support"

}
ENGINEERS = [

    "Rahul Sharma",
    "Priya Verma",
    "Arjun Reddy",
    "Sneha Patel",
    "Amit Kumar",
    "Neha Singh",
    "Kiran Rao",
    "Swathi Reddy",
    "Vikram Gupta",
    "Pooja Nair",
    "Deepak Mishra",
    "Suresh Kumar",
    "Anjali Das",
    "Rohit Jain",
    "Manoj Joshi",
    "Nikhil Rao",
    "Divya Sharma",
    "Rakesh Patel",
    "Akash Verma",
    "Harsha Kumar"

]
def random_date(start_date: datetime, end_date: datetime) -> datetime:
    """
    Generate a random datetime between start_date and end_date.
    """
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86400)
    return start_date + timedelta(days=random_days, seconds=random_seconds)
def generate_users(num_users: int) -> pd.DataFrame:
    """
    Generate synthetic employee data.
    """

    logger.info("Generating Users...")

    users = []

    for i in range(1, num_users + 1):

        name = fake.name()

        users.append({

            "employee_id": f"EMP{i:05d}",

            "employee_name": name,

            "employee_email": name.lower().replace(" ", ".").replace("'", "") + "@abctech.com",

            "department": random.choice(DEPARTMENTS),

            "location": random.choice(LOCATIONS),

            "joining_date": random_date(
                datetime(2018,1,1),
                datetime(2025,1,1)
            ).date(),

            "vip_user": random.choice(["Yes","No"]),

            "phone": fake.phone_number()

        })

    users_df = pd.DataFrame(users)

    users_df.to_csv(
        os.path.join(DATA_DIR,"users.csv"),
        index=False
    )

    logger.info(f"{len(users_df)} Users Generated")

    return users_df
def generate_assets(num_assets: int) -> pd.DataFrame:
    """
    Generate company assets.
    """

    logger.info("Generating Assets...")

    manufacturers = [

        "Dell",

        "HP",

        "Lenovo",

        "Apple",

        "Asus",

        "Acer"

    ]

    assets = []

    for i in range(1, num_assets + 1):

        purchase_year = random.randint(2019,2025)

        assets.append({

            "asset_id":f"AST{i:05d}",

            "asset_name":fake.word().upper()+"-"+str(random.randint(1000,9999)),

            "device_type":random.choice(DEVICE_TYPES),

            "manufacturer":random.choice(manufacturers),

            "purchase_year":purchase_year,

            "warranty_status":random.choice([

                "Active",

                "Expired"

            ]),

            "location":random.choice(LOCATIONS)

        })

    assets_df = pd.DataFrame(assets)

    assets_df.to_csv(

        os.path.join(DATA_DIR,"assets.csv"),

        index=False

    )

    logger.info(f"{len(assets_df)} Assets Generated")

    return assets_df
def generate_engineers() -> pd.DataFrame:
    """
    Generate IT support engineers.
    """

    logger.info("Generating Engineers...")

    engineer_data = []

    specializations = [

        "Hardware",

        "Software",

        "Network",

        "Security",

        "Cloud",

        "Database",

        "Printer",

        "Email",

        "Account",

        "Mobile"

    ]

    for i, engineer in enumerate(ENGINEERS, start=1):

        engineer_data.append({

            "engineer_id":f"ENG{i:03d}",

            "engineer_name":engineer,

            "experience_years":random.randint(2,15),

            "specialization":random.choice(specializations),

            "rating":round(random.uniform(3.5,5.0),1)

        })

    engineer_df = pd.DataFrame(engineer_data)

    engineer_df.to_csv(

        os.path.join(DATA_DIR,"engineers.csv"),

        index=False

    )

    logger.info(f"{len(engineer_df)} Engineers Generated")

    return engineer_df

# ============================
# PRIORITY CALCULATION
# ============================

def calculate_priority(impact, urgency):
    """
    Calculate ticket priority based on ITIL matrix.
    """

    matrix = {
        ("High", "High"): "Critical",
        ("High", "Medium"): "High",
        ("High", "Low"): "High",
        ("Medium", "High"): "High",
        ("Medium", "Medium"): "Medium",
        ("Medium", "Low"): "Medium",
        ("Low", "High"): "Medium",
        ("Low", "Medium"): "Low",
        ("Low", "Low"): "Low"
    }

    return matrix[(impact, urgency)]
# ============================
# RESOLUTION HOURS
# ============================

def resolution_hours(priority):

    if priority == "Critical":
        return round(random.uniform(0.5, 4), 2)

    elif priority == "High":
        return round(random.uniform(2, 8), 2)

    elif priority == "Medium":
        return round(random.uniform(8, 24), 2)

    else:
        return round(random.uniform(24, 72), 2)
ROOT_CAUSES = [

    "Configuration Error",

    "User Mistake",

    "Hardware Failure",

    "Software Bug",

    "Network Congestion",

    "Expired Certificate",

    "Database Lock",

    "Memory Leak",

    "Disk Failure",

    "Security Policy",

    "Unknown"

]
RESOLUTION_NOTES = [

    "Restarted the affected service.",

    "Installed latest software updates.",

    "Replaced faulty hardware component.",

    "Reset user password and unlocked account.",

    "Restarted VPN service.",

    "Updated printer drivers.",

    "Cleared application cache.",

    "Increased disk space.",

    "Reconfigured network settings.",

    "Escalated to Level 2 Support.",

    "Applied security patch.",

    "Restarted database server."

]
def create_description(issue, department):

    templates = [

        f"User from {department} department reported that {issue.lower()}. Daily work is affected.",

        f"{department} employee cannot continue work because {issue.lower()}.",

        f"Incident reported from {department}. Problem: {issue.lower()}.",

        f"A user in {department} raised a ticket stating that {issue.lower()}.",

        f"Business process interrupted because {issue.lower()}."

    ]

    return random.choice(templates)
def generate_incidents(users_df,
                       assets_df,
                       engineers_df):

    logger.info("Generating Incidents...")

    incidents = []

    engineer_lookup = engineers_df.to_dict("records")

    users = users_df.to_dict("records")

    assets = assets_df.to_dict("records")

    for i in range(1, NUM_INCIDENTS + 1):

        category = random.choice(list(CATEGORIES.keys()))

        issue = random.choice(CATEGORIES[category])

        user = random.choice(users)

        asset = random.choice(assets)

        engineer = random.choice(engineer_lookup)

        impact = random.choice(IMPACT)

        urgency = random.choice(URGENCY)

        priority = calculate_priority(impact, urgency)

        created = random_date(
            START_DATE,
            END_DATE
        )

        hours = resolution_hours(priority)

        resolved = created + timedelta(hours=hours)

        assignment_group = ASSIGNMENT_GROUPS[category]

        incidents.append({

            "incident_number":f"INC{i:06d}",

            "created_date":created,

            "resolved_date":resolved,

            "employee_id":user["employee_id"],

            "employee_name":user["employee_name"],

            "department":user["department"],

            "location":user["location"],

            "asset_id":asset["asset_id"],

            "device_type":asset["device_type"],

            "short_description":issue,

            "description":create_description(
                issue,
                user["department"]
            ),

            "category":category,

            "impact":impact,

            "urgency":urgency,

            "priority":priority,

            "assignment_group":assignment_group,

            "assigned_engineer":engineer["engineer_name"],

            "status":random.choice(STATUS),

            "sla_status":random.choice(
                [
                    "Within SLA",
                    "Breached"
                ]
            ),

            "resolution_time_hours":hours,

            "resolution_notes":random.choice(
                RESOLUTION_NOTES
            ),

            "root_cause":random.choice(
                ROOT_CAUSES
            ),

            "customer_satisfaction":random.randint(1,5)

        })

    incidents_df = pd.DataFrame(incidents)

    incidents_df.to_csv(

        os.path.join(DATA_DIR,"incidents.csv"),

        index=False

    )

    logger.info(

        f"{len(incidents_df)} Incidents Generated"

    )

    return incidents_df
if __name__ == "__main__":

    logger.info("Generating Enterprise Dataset")

    users_df = generate_users(NUM_USERS)

    assets_df = generate_assets(NUM_ASSETS)

    engineers_df = generate_engineers()

    incidents_df = generate_incidents(

        users_df,

        assets_df,

        engineers_df

    )

    print("\nDataset Generation Completed Successfully")

    print(f"Users      : {len(users_df)}")

    print(f"Assets     : {len(assets_df)}")

    print(f"Engineers  : {len(engineers_df)}")

    print(f"Incidents  : {len(incidents_df)}")
