from fastapi import FastAPI
from search import search

app = FastAPI()

@app.get("/search")
def semantic_search(query: str):
    results = search(query)
    return {"results": results}