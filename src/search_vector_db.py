import pickle
import faiss
from sentence_transformers import SentenceTransformer

# Load FAISS index
index = faiss.read_index("vector_db/knowledge.index")

# Load Knowledge Base
with open("vector_db/knowledge.pkl", "rb") as f:
    kb = pickle.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query, top_k=3):
    embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        embedding,
        top_k
    )

    return kb.iloc[indices[0]]