import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load Knowledge Base
kb = pd.read_csv("data/knowledge_base.csv")

print(kb.head())
print("Knowledge Base Shape:", kb.shape)

# Load Sentence Transformer Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create Embeddings
embeddings = model.encode(
    kb["issue"].tolist(),
    convert_to_numpy=True
)

print("Embeddings Shape:", embeddings.shape)

# Create FAISS Index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("Knowledge Base Indexed Successfully")


# -----------------------------
# Search Function
# -----------------------------
def search_issue(query, top_k=3):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    return kb.iloc[indices[0]]


# -----------------------------
# Test 1
# -----------------------------
results = search_issue("VPN keeps disconnecting")

print("\nTop Matches for: VPN keeps disconnecting\n")

for _, row in results.iterrows():
    print("=" * 60)
    print("Issue:", row["issue"])
    print("Category:", row["category"])
    print("Root Cause:", row["root_cause"])
    print("Resolution:", row["resolution"])
    print("Assignment Group:", row["assignment_group"])
    print("=" * 60)


# -----------------------------
# Test 2
# -----------------------------
results = search_issue("Laptop not booting")

print("\nTop Matches for: Laptop not booting\n")

for _, row in results.iterrows():
    print("=" * 60)
    print("Issue:", row["issue"])
    print("Category:", row["category"])
    print("Root Cause:", row["root_cause"])
    print("Resolution:", row["resolution"])
    print("Assignment Group:", row["assignment_group"])
    print("=" * 60)