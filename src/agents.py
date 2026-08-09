from typing import TypedDict
import joblib
import pandas as pd

print("Step 1: Imports started")

from preprocessing import clean_text
print("✓ preprocessing imported")

from search_vector_db import search
print("✓ search_vector_db imported")


# -----------------------------
# Load Models
# -----------------------------
print("Loading Category Model...")
category_model = joblib.load("models/category_model.pkl")
print("✓ Category Model Loaded")

print("Loading Priority Model...")
priority_model = joblib.load("models/priority_model.pkl")
print("✓ Priority Model Loaded")

print("Loading TF-IDF...")
tfidf = joblib.load("models/tfidf.pkl")
print("✓ TF-IDF Loaded")


# -----------------------------
# Agent State
# -----------------------------
class AgentState(TypedDict):
    incident: str
    category: str
    priority: str
    resolution: str
    assignment_group: str


# -----------------------------
# Incident Analyzer Agent
# -----------------------------
def incident_agent(state):
    print("\n========== INCIDENT ANALYZER ==========")
    print("Incident Received:")
    print(state["incident"])
    return state


# -----------------------------
# Category Prediction Agent
# -----------------------------
def category_agent(state):

    cleaned = clean_text(state["incident"])

    vector = tfidf.transform([cleaned])

    prediction = category_model.predict(vector)[0]

    state["category"] = prediction

    print("\n========== CATEGORY AGENT ==========")
    print("Predicted Category:", prediction)

    return state


# -----------------------------
# Priority Prediction Agent
# -----------------------------
def priority_agent(state):

    sample = pd.DataFrame([
        {
            "description": state["incident"],
            "impact": "Medium",
            "urgency": "Medium"
        }
    ])

    prediction = priority_model.predict(sample)[0]

    state["priority"] = prediction

    print("\n========== PRIORITY AGENT ==========")
    print("Predicted Priority:", prediction)

    return state


# -----------------------------
# Knowledge Retrieval Agent
# -----------------------------
def knowledge_agent(state):

    results = search(state["incident"], top_k=1)

    row = results.iloc[0]

    state["resolution"] = row["resolution"]
    state["assignment_group"] = row["assignment_group"]

    print("\n========== KNOWLEDGE AGENT ==========")
    print("Issue Found :", row["issue"])
    print("Resolution :", row["resolution"])
    print("Assignment Group :", row["assignment_group"])

    return state


# -----------------------------
# Decision Agent
# -----------------------------
def decision_agent(state):

    print("\n========== FINAL DECISION ==========")

    print("Incident:")
    print(state["incident"])

    print("\nCategory:")
    print(state["category"])

    print("\nPriority:")
    print(state["priority"])

    print("\nAssignment Group:")
    print(state["assignment_group"])

    print("\nSuggested Resolution:")
    print(state["resolution"])

    print("\nTicket Ready For ServiceNow")

    return state


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    print("\nStarting Agent Workflow...\n")

    state = {
        "incident": "VPN not connecting to company network",
        "category": "",
        "priority": "",
        "resolution": "",
        "assignment_group": ""
    }

    state = incident_agent(state)
    state = category_agent(state)
    state = priority_agent(state)
    state = knowledge_agent(state)
    state = decision_agent(state)

    print("\nWorkflow Completed Successfully!")