from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag import answer_question   # import the RAG engine

app = FastAPI(title="Store Support Agent")

# Allow the Next.js frontend to call this API from the browser.
# Scoped to just the frontend's dev URLs — not open to every site.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


# Shape of an incoming request body: {"question": "..."}
class Query(BaseModel):
    question: str


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Support agent is running."}


@app.post("/ask")
def ask(query: Query):
    answer = answer_question(query.question)
    return {"question": query.question, "answer": answer}