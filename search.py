import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("models/log_index.faiss")

# You must call the function and assign its return value to 'unique_logs'

with open("models/logs.pkl", "rb") as f:
    all_logs = pickle.load(f)

def clean_query(q):
    return q.lower().strip()


def search(query, k=10, threshold=0.3):

    query = clean_query(query)

    query_vec = model.encode([query])
    query_vec = np.array(query_vec).astype("float32")

    # Normalize
    query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)

    distances, indices = index.search(query_vec, k)

    results = []

    for score, idx in zip(distances[0], indices[0]):
        if score >= threshold:
            results.append({
                "text": all_logs[idx]["text"],
                "source": all_logs[idx]["source"],
                "score": float(score)
            })

    # Sort النتائج (optional but good)
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    # Handle empty results
    if not results:
        return [{
            "text": "No relevant results found",
            "source": "none",
            "score": 0
        }]

    return results