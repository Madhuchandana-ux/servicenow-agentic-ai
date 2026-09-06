import os
import pickle
from functools import lru_cache


def _abs_path(*parts):
    """Helper to build a path relative to repo root."""
    base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_db")
    return os.path.join(base, *parts)


@lru_cache(maxsize=1)
def _load_vector_db():
    """Lazy-load FAISS index, pickled KB and embedding model.

    Raises RuntimeError with guidance if files missing.
    """
    try:
        import faiss
        from sentence_transformers import SentenceTransformer
    except Exception as e:
        raise RuntimeError("FAISS and sentence-transformers are required for the vector DB: install the project requirements") from e

    index_path = _abs_path("knowledge.index")
    pickle_path = _abs_path("knowledge.pkl")

    if not os.path.exists(index_path) or not os.path.exists(pickle_path):
        raise RuntimeError(
            "Vector DB artifacts not found. Run src/build_vector_db.py to create vector_db/knowledge.index and vector_db/knowledge.pkl"
        )

    index = faiss.read_index(index_path)

    with open(pickle_path, "rb") as f:
        kb = pickle.load(f)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    return index, kb, model


def search(query, top_k=3):
    """Return pandas DataFrame rows of top matches.

    Raises RuntimeError if vector DB artifacts are missing.
    """
    index, kb, model = _load_vector_db()

    embedding = model.encode([query], convert_to_numpy=True)

    distances, indices = index.search(embedding, top_k)

    return kb.iloc[indices[0]]
