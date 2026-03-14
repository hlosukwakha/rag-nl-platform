from fastapi import FastAPI
from pydantic import BaseModel
from apps.api.rag import RAGService

app = FastAPI(title="rag-nl-platform")
service = RAGService()

class AskRequest(BaseModel):
    question: str
    top_k: int = 5

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskRequest):
    return service.answer(req.question, req.top_k)

@app.get("/sources")
def sources():
    return service.list_sources()
