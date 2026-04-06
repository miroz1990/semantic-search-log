from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from read_all_logs import read_Logs
from read_all_logs import deduplicate_logs
import pandas as pd

# -------------------------------
# Step 4: Initialize model and prepare data
# -------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Creating embeddings...")

df = pd.read_csv("data/logs_with_queries.csv")
log_texts = df['text'].astype(str).tolist()

logs_metadata = df[['text', 'source']].to_dict('records')

# You must call the function and assign its return value to 'unique_logs'
# raw_logs  = read_Logs()
# unique_logs=deduplicate_logs(raw_logs)

# -------------------------------
# Step 5: Create embeddings for logs
# -------------------------------

# texts = [log["text"] for log in unique_logs]
embeddings = model.encode(log_texts, show_progress_bar=True)

# embeddings = model.encode(texts, show_progress_bar=True)

# Normalize embeddings to unit length
embeddings = np.array(embeddings).astype("float32")

embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

# -------------------------------
# Step 6: Build FAISS index
# -------------------------------
dimension = embeddings.shape[1]
faiss.normalize_L2(embeddings)
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

print("Total vectors in index:", index.ntotal)

# -------------------------------
# Step 7: Save index and metadata
# -------------------------------
faiss.write_index(index, "models/log_index.faiss")

with open("models/logs.pkl", "wb") as f:
    pickle.dump(logs_metadata, f)

print("✅ Index and logs saved successfully!")