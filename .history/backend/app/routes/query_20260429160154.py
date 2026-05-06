from fastapi import APIRouter

router = APIRouter()


@router.post("/query")
async def query_llm(question: str):
    return {
        "question": question,
        "answer": "This is a placeholder response (LLM not connected yet)"
    }
