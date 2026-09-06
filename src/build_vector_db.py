import json
import os
import subprocess
from datetime import datetime

def get_git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
    except Exception:
        return "unknown"

def build_vector_db():
    os.makedirs("vector_db", exist_ok=True)
    
    # Placeholder for vector index creation
    with open("vector_db/index.placeholder", "w") as f:
        f.write("faiss_index_placeholder")

    metadata = {
        "created_date": datetime.utcnow().isoformat(),
        "git_commit": get_git_commit(),
        "vector_count": 0,
        "index_path": "vector_db/index.placeholder"
    }

    with open("vector_db/vector_db.metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print("Vector DB metadata written successfully.")

if __name__ == "__main__":
    build_vector_db()
