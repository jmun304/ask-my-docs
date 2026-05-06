from fastapi import APIRouter
from pydantic import BaseModel
from app.services.retrieval import retrieve_chunks

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    doc_id: str = None

@router.post("/query")
async def query_llm(request: QueryRequest):
    chunks = retrieve_chunks(request.question, request.doc_id)
    return {
        "question": request.question,
        "chunks": chunks
    }