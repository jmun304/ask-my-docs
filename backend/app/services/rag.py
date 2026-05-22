"""
This file contains the core RAG (Retrieval-Augmented Generation) pipeline.

- Retrieved chunks will be passed into an LLM (e.g., OpenAI, Anthropic, etc.)
- The LLM will generate a final natural language answer using:
    1. The user question
    2. The retrieved context chunks

Pipeline:
    question → retrieve_chunks → LLM → answer
"""

from app.services.retrieval import retrieve_chunks
from app.services.llm import build_prompt, generate_response


def rag_pipeline(question: str):
    """
    Main RAG pipeline entry point.

    Args:
        question (str): User query about the document.

    Returns:
        dict: Contains:
            - answer (str or None): Final answer (LLM output in future)
            - context (list[str]): Retrieved document chunks used for generation
    """

    # Step 1: Retrieve relevant chunks from vector database
    # This is the "Retrieval" part of RAG
    chunks = retrieve_chunks(question)

    # Step 2: Handle empty retrieval case (Guardrail)
    # If no relevant chunks are found, we avoid calling the LLM later
    if not chunks:
        return {
            "answer": "No relevant information found in the document.",
            "context": []
        }

    # Step 3: LLM integration
    # - Build prompt using question + chunks
    # - Send to LLM API (OpenAI / local model)
    # - Parse response into "answer"

    prompt = build_prompt(question, chunks)
    answer = generate_response(prompt)

    return {
        "answer": answer,
        "context": chunks
    }
