"""
This file defines the /query API endpoint.

========================================================
CURRENT STATE (MVP - CORRECT IMPLEMENTATION)
========================================================
- Receives a user question
- Passes the question to rag_pipeline()
- rag_pipeline() handles:
    → retrieval (vector search)
    → returns relevant context chunks
- API returns:
    → question
    → retrieved context (no LLM yet)

CURRENT CORRECT FLOW:
    request → rag_pipeline → retrieval → response

========================================================
IMPORTANT ARCHITECTURAL RULE (DO NOT BREAK)
========================================================
DO NOT bypass rag_pipeline() in this file.

❌ BEFORE: chunks = retrieve_chunks(request.question)
    Code above:
    - Bypasses the RAG orchestration layer
    - Mixes API layer with retrieval logic
    - Prevents clean LLM integration later
    - Duplicates logic already handled in rag.py

✔ CORRECT APPROACH:
    Always call:
        rag_pipeline(request.question)

========================================================
FUTURE STATE (WITH LLM INTEGRATION)
========================================================
- rag_pipeline() will expand to include:
    1. retrieve relevant chunks
    2. construct prompt
    3. call LLM (OpenAI / local model)
    4. return generated answer

FUTURE FLOW:
    request → rag_pipeline → retrieval + LLM → final answer

IMPORTANT:
- query.py will NOT change when LLM is added
- ONLY rag.py will be modified
"""

from fastapi import APIRouter
from app.models.schema import QueryRequest, QueryResponse
from app.services.rag import rag_pipeline

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_docs(request: QueryRequest):
    """
    API endpoint for asking questions about the uploaded document.

    This endpoint is intentionally "thin":
    it delegates ALL logic to the RAG pipeline.

    Args:
        request (QueryRequest): User's question input

    Returns:
        QueryResponse:
            - question: original user question
            - answer: LLM-generated answer (None in MVP stage)
            - context_used: retrieved chunks used for answering
    """

    # =====================================================
    # CORRECT IMPLEMENTATION (DO NOT REPLACE THIS)
    # =====================================================
    result = rag_pipeline(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "context_used": result["context"]
    }