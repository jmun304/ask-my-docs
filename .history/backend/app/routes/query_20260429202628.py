from fastapi import APIRouter
from pydantic import BaseModel
from app.services.retrieval import retrieve_chunks

router = APIRouter()

class QueryRequest(BaseModel):#question format must be str
    question: str

@router.post("/query")
async def query_llm(request: QueryRequest):
    chunks = retrieve_chunks(request.question)
    return {
        "question": request.question,
        "chunks": chunks
    }