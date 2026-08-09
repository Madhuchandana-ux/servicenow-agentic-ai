import pandas as pd
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os

# Load Knowledge Base
kb = pd.read_csv("data/knowledge_base.csv")

# Load Embedding Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create Embeddings
embeddings = model.encode(
    kb["issue"].tolist(),
    convert_to_numpy=True
)

# Create FAISS Index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

os.makedirs("vector_db", exist_ok=True)

# Save FAISS Index
faiss.write_index(index, "vector_db/knowledge.index")

# Save Knowledge Base
with open("vector_db/knowledge.pkl", "wb") as f:
    pickle.dump(kb, f)

print("Vector Database Saved Successfully!")