import logging
import os
from functools import lru_cache
from typing import TypedDict

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def load_models():
    """Lazy-load ML models and vectorizers from the models/ directory.

    Returns a dict with keys: category_model, priority_model, tfidf
    Raises RuntimeError with actionable message if artifacts are missing.
    """
    try:
        import joblib
    except Exception as e:
        raise RuntimeError(
            "joblib is required to load models: install the project requirements"
        ) from e

    model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

    category_path = os.path.join(model_dir, "category_model.pkl")
    priority_path = os.path.join(model_dir, "priority_model.pkl")
    tfidf_path = os.path.join(model_dir, "tfidf.pkl")

    missing = [
        p for p in (category_path, priority_path, tfidf_path) if not os.path.exists(p)
    ]
    if missing:
        msg = (
            "Missing model artifacts: {}. Run the training "
            "scripts in src/ to generate models or place them "
            "in the models/ directory."
        )
        raise RuntimeError(msg.format(", ".join(missing)))

    category_model = joblib.load(category_path)
    priority_model = joblib.load(priority_path)
    tfidf = joblib.load(tfidf_path)

    logger.info("Loaded models from %s", model_dir)

    return {
        "category_model": category_model,
        "priority_model": priority_model,
        "tfidf": tfidf,
    }


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
def incident_agent(state: AgentState) -> AgentState:
    logger.info("Incident received")
    logger.debug("Incident text: %s", state.get("incident"))
    return state


# -----------------------------
# Category Prediction Agent
# -----------------------------
def category_agent(state: AgentState) -> AgentState:
    from src.preprocessing import clean_text

    cleaned = clean_text(state["incident"])

    models = load_models()
    tfidf = models["tfidf"]
    category_model = models["category_model"]

    vector = tfidf.transform([cleaned])
    prediction = category_model.predict(vector)[0]

    state["category"] = prediction

    logger.info("Predicted category: %s", prediction)

    return state


# -----------------------------
# Priority Prediction Agent
# -----------------------------
def priority_agent(state: AgentState) -> AgentState:
    import pandas as pd

    models = load_models()
    priority_model = models["priority_model"]

    sample = pd.DataFrame(
        [
            {
                "description": state["incident"],
                "impact": "Medium",
                "urgency": "Medium",
            }
        ]
    )

    prediction = priority_model.predict(sample)[0]

    state["priority"] = prediction

    logger.info("Predicted priority: %s", prediction)

    return state


# -----------------------------
# Knowledge Retrieval Agent
# -----------------------------
def knowledge_agent(state: AgentState) -> AgentState:
    from src.search_vector_db import search

    try:
        results = search(state["incident"], top_k=1)
    except RuntimeError as e:
        logger.warning("Vector DB unavailable: %s", e)
        state["resolution"] = "No recommended resolution found (KB unavailable)"
        state["assignment_group"] = ""
        return state

    if results is None or results.empty:
        logger.warning("No knowledge base match found for incident")
        state["resolution"] = "No recommended resolution found"
        state["assignment_group"] = ""
        return state

    row = results.iloc[0]

    state["resolution"] = row.get("resolution", "")
    state["assignment_group"] = row.get("assignment_group", "")

    logger.info("Knowledge retrieved: issue=%s", row.get("issue"))

    return state


# -----------------------------
# Decision Agent
# -----------------------------
def decision_agent(state: AgentState) -> AgentState:
    logger.info("Final decision prepared for ticket creation")
    return state


# -----------------------------
# Main (for local debugging)
# -----------------------------
if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)

    state: AgentState = {
        "incident": "VPN not connecting to company network",
        "category": "",
        "priority": "",
        "resolution": "",
        "assignment_group": "",
    }

    state = incident_agent(state)
    state = category_agent(state)
    state = priority_agent(state)
    state = knowledge_agent(state)
    state = decision_agent(state)

    print("Workflow Completed Successfully!")
