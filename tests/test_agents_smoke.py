import pytest
from src import agents


def test_agents_flow_monkeypatch(monkeypatch):
    # Dummy TFIDF and models
    class DummyTFIDF:
        def transform(self, x):
            return x

    class DummyCategoryModel:
        def predict(self, x):
            return ["Network"]

    class DummyPriorityModel:
        def predict(self, df):
            return ["High"]

    dummy_models = {
        "category_model": DummyCategoryModel(),
        "priority_model": DummyPriorityModel(),
        "tfidf": DummyTFIDF(),
    }

    monkeypatch.setattr(agents, "load_models", lambda: dummy_models)

    state = {
        "incident": "VPN is down",
        "category": "",
        "priority": "",
        "resolution": "",
        "assignment_group": "",
    }

    state = agents.incident_agent(state)
    state = agents.category_agent(state)
    state = agents.priority_agent(state)

    assert state["category"] == "Network"
    assert state["priority"] == "High"
