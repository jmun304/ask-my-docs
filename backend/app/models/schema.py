"""
This file defines the API data contracts for the application.

We use Pydantic BaseModel classes to:
- Validate incoming request data (what the frontend sends)
- Standardize outgoing response data (what the backend returns)
- Ensure consistency across all routes
- Provide automatic API documentation via FastAPI (Swagger UI)

IMPORTANT:
- This is the SINGLE source of truth for API request/response shapes.
- Do NOT redefine models inside route files.
- Any changes here will affect both backend validation and frontend expectations.
"""

from pydantic import BaseModel


class QueryRequest(BaseModel):
    """
    Input model for /query endpoint.

    Attributes:
        question (str): The user's question about the uploaded document.
    """
    question: str


class QueryResponse(BaseModel):
    """
    Output model for /query endpoint.

    Attributes:
        question (str): The original user question.
        answer (str): Generated answer (currently placeholder until LLM integration).
        context_used (list[str]): Retrieved text chunks used to generate the answer.
    """
    question: str
    answer: str
    context_used: list[str]
