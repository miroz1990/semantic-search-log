import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import re

# =========================
# Load Models & Data
# =========================
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("models/log_index.faiss")

df = pd.read_csv("data/logs_with_queries.csv")

# Clean text helper
def clean_text(text):
    if not isinstance(text, str): return ""
    return " ".join(re.sub(r'[^a-z0-9\s]', '', text.lower()).split())

def clean_query(q):
    return q.lower().strip()

df['clean_text'] = df['text'].apply(clean_text)
logs = df[['text', 'clean_text', 'source']].to_dict('records')

# NEW: Group all valid logs by their generated query
query_groups = {}
for _, row in df.iterrows():
    q = row["generated_query"].strip()
    if q not in query_groups:
        query_groups[q] = {
            "valid_logs": [],
            "expected_sources": set()
        }
    query_groups[q]["valid_logs"].append(row["clean_text"])
    query_groups[q]["expected_sources"].add(str(row["source"]).strip().lower())

# =========================
# Search Function
# =========================
def search(query, top_k=10):
    query = clean_query(query)
    query_emb = model.encode([query]).astype("float32")

    # Normalize
    query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)

    D, I = index.search(query_emb, top_k)
    results = []
    for dist, idx in zip(D[0], I[0]):
        if idx != -1 and idx < len(logs):
            results.append({
                "text": logs[idx]["text"],
                "clean_text": logs[idx]["clean_text"],
                "source": logs[idx]["source"],
                "dist": float(dist)
            })
    return results

# =========================
# Evaluation Loop (Group-Aware)
# =========================
precisions = []
mrrs = []
source_accs = []

print(f"Evaluating {len(query_groups)} unique queries...")

for query_text, data in query_groups.items():
    results = search(query_text, top_k=10)
    
    valid_list = data["valid_logs"]
    valid_sources = data["expected_sources"]
    
    found_at = -1
    for i, r in enumerate(results):
        # Check if the result matches ANY of the valid logs for this query
        if any(v == r["clean_text"] or v in r["clean_text"] or r["clean_text"] in v for v in valid_list):
            found_at = i
            break
    
    # Hit Rate @ 5
    precisions.append(1 if (found_at != -1 and found_at < 5) else 0)
    
    # Reciprocal Rank
    mrrs.append(1 / (found_at + 1) if found_at != -1 else 0)
    
    # Source Accuracy (Top 1)
    sa = 0
    if results and results[0]["source"].lower() in valid_sources:
        sa = 1
    source_accs.append(sa)

print("\n========== Grouped Evaluation Results ==========")
print(f"Unique Queries:  {len(query_groups)}")
print(f"Hit Rate@5:      {np.mean(precisions):.3f}")
print(f"MRR:             {np.mean(mrrs):.3f}")
print(f"Source Accuracy: {np.mean(source_accs):.3f}")

# Manual Quick Test
test_q = "Search for logs regarding error env createbean2 factory error..."
print(f"\nManual Test: '{test_q}'")
res = search(test_q, top_k=3)
for i, r in enumerate(res):
    print(f"{i+1}. [Dist: {r['dist']:.4f}] ({r['source']}) {r['text']}")