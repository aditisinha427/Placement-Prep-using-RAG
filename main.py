
from fastapi import FastAPI
from rag import load_db, get_answer

app = FastAPI()

db = load_db()

@app.get("/")
def home():
    return {"message": "Placement Prep Copilot Running 🚀"}

@app.get("/ask")
def ask(query: str):
    answer = get_answer(query, db)
    return {
        "question": query,
        "answer": answer
    }