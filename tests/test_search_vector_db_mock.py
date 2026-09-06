import pandas as pd
from src import search_vector_db as svd


def dummy_load_vector_db():
    kb = pd.DataFrame([{"issue": "VPN problem", "resolution": "Restart VPN", "assignment_group": "Network Support"}])
    class DummyIndex:
        def search(self, embedding, top_k):
            # return distances and indices shaped like FAISS output
            distances = [[0.0]]
            indices = [[0]]
            return distances, indices
    class DummyModel:
        def encode(self, texts, convert_to_numpy=False):
            return [[0.1, 0.2]]
    return DummyIndex(), kb, DummyModel()


def test_search_monkeypatch(monkeypatch):
    monkeypatch.setattr(svd, "_load_vector_db", lambda: dummy_load_vector_db())
    res = svd.search("VPN issue", top_k=1)
    assert not res.empty
    assert "resolution" in res.columns
