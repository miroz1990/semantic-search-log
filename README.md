# 🔍 Semantic Search for System Logs (FAISS + NLP)

A production-style **semantic search engine for system logs** using **Sentence Transformers + FAISS**, with evaluation and query generation support.

---

## 🚀 Project Overview

This project enables **semantic understanding of system logs**, allowing users to search using natural language queries instead of exact keywords.

It also leverages a **query-generation dataset** to simulate realistic user search behavior.

---

## 🧠 Key Features

* 🔎 Semantic search using Sentence Transformers
* ⚡ Fast similarity search with FAISS
* 📊 Evaluation metrics:

  * Precision@K
  * Mean Reciprocal Rank (MRR)
  * Source Accuracy
* 🧪 Query-based evaluation using real/generated queries
* 🌐 API (FastAPI) for serving search
* 🖥️ Streamlit UI for interactive search

---

## 📁 Important Dataset

### `data/logs_with_queries.csv`

This is a **core dataset** used for evaluation and testing.

Each row contains:

* `text` → original log
* `source` → log source (Apache / HDFS / Linux)
* `embeddings` → precomputed vector
* `cluster` → cluster ID
* `generated_query` → **natural language query mapped to the log**

### Example:

```
Log:
error env createbean2 factory error creating worker jni onstartup...

Query:
Search for logs regarding error env createbean2 factory error...
```

👉 This allows realistic evaluation of semantic search performance.

---

## ⚙️ How It Works

### 1. Data Preparation

* Logs are cleaned and deduplicated
* Queries are generated and stored in `logs_with_queries.csv`

---

### 2. Embedding Generation

* Logs → embeddings using Sentence Transformers

---

### 3. Indexing (FAISS)

* Store embeddings in FAISS index for fast retrieval

---

### 4. Query Search

* Convert query → embedding
* Retrieve top-k similar logs
* Apply similarity threshold (e.g., `score > 0.45`)

---

### 5. Evaluation

* Uses query-log pairs from dataset
* Measures:

  * Precision@5
  * MRR
  * Source Accuracy

---

## 📊 Example Query

### 🔍 Query:

```
Search for logs regarding error env createbean2 factory error...
```

### ✅ Expected Semantic Results:

```
error env createbean2 factory error creating worker jni onstartup
error config update can't create worker jni onstartup
```

👉 Semantic search successfully captures **context ("createbean", "worker", "error")**, even if wording differs.

---

## 📈 Evaluation Results

```
Precision@5:     0.400
MRR:             0.511
Source Accuracy: 0.889
```

---

## 🧠 Insights

* ✅ Semantic search understands **meaning, not just keywords**
* ✅ Works well with **noisy and unstructured logs**
* 🔥 Strong performance in **realistic query scenarios**

---

## 🛠️ Installation

```bash
git clone <your-repo-url>
cd semantic_search_logs

pip install -r requirements.txt
```

---

## ▶️ Usage

### Build FAISS index

```bash
python create_embeddings.py
```

### Run search

```bash
python search.py
```

### Run evaluation

```bash
python evaluation/evaluate.py
```

### Run API

```bash
uvicorn api.main:app --reload
```

### Run Streamlit UI

```bash
streamlit run streamlit_app.py
```

---

## 📈 Future Improvements

* 🔄 Hybrid Search (Semantic + Keyword-based)
* 📊 BM25 baseline
* 🤖 Better embedding models
* ⚙️ Automatic threshold tuning
* ☁️ Deployment (Docker / Cloud)

---

## 🛠️ Core Competencie

This project demonstrates:

* NLP & Semantic Search
* Vector Search (FAISS)
* Information Retrieval Metrics
* End-to-End ML Pipeline
* API Development

---

## 🧑‍💻 Author

**Ameer Omar**
