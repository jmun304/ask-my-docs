"""
This file contains the core RAG (Retrieval-Augmented Generation) pipeline.

CURRENT STATE (MVP):
- Only performs retrieval from the vector database
- No LLM integration yet
- Returns retrieved context chunks for debugging and frontend display

FUTURE STATE (LLM INTEGRATION):
- Retrieved chunks will be passed into an LLM (e.g., OpenAI, Anthropic, etc.)
- The LLM will generate a final natural language answer using:
    1. The user question
    2. The retrieved context chunks

Pipeline will become:
    question → retrieve_chunks → LLM → answer
"""

from app.services.retrieval import retrieve_chunks


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

    # Step 3: Placeholder for LLM integration
    # FUTURE IMPLEMENTATION:
    # - Build prompt using question + chunks
    # - Send to LLM API (OpenAI / local model)
    # - Parse response into "answer"
    #
    # Example future code:
    #
    # prompt = build_prompt(question, chunks)
    # answer = llm.generate(prompt)
    #
    # return {
    #     "answer": answer,
    #     "context": chunks
    # }

    return {
        "answer": "LLM not integrated yet (MVP mode). Retrieved context only.",  # LLM integration will replace this
        "context": chunks
    }
