# System Architecture

## Data Flow
1. User Query -> Streamlit UI
2. Classification Agent -> LogisticRegression + TF-IDF
3. Priority Agent -> RandomForest
4. Knowledge Retrieval -> FAISS Index + SentenceTransformers
5. Action Agent -> ServiceNow REST API
