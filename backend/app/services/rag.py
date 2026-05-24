"""
This file contains the core RAG (Retrieval-Augmented Generation) pipeline.

CURRENT STATE (LLM INTEGRATED):
- Retrieves relevant chunks from the vector database
- Builds a prompt using the question and retrieved chunks
- Calls Groq LLM to generate a final answer

PIPELINE:
    question → retrieve_chunks → build_prompt → Groq LLM → answer
"""

import os
from groq import Groq
from app.services.retrieval import retrieve_chunks

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(question: str, chunks: list[str]) -> str:
    """
    Builds a prompt for the LLM using the question and retrieved chunks.

    Args:
        question (str): User query about the document.
        chunks (list[str]): Retrieved context chunks from vector database.

    Returns:
        str: Formatted prompt to send to the LLM.
    """
    context = "\n\n".join(chunks)
    return f"""You are a helpful assistant. Answer the question as thoroughly as possible using only the context provided below.
    - Use all relevant information from the context
    - If multiple chunks mention the topic, combine them into a complete answer
    - Use bullet points or numbered lists when listing multiple points
    - If the answer is not in the context, say "I could not find the answer in the document."

Context:
{context}

Question: {question}

Answer:"""


def rag_pipeline(question: str) -> dict:
    """
    Main RAG pipeline entry point.

    Args:
        question (str): User query about the document.

    Returns:
        dict: Contains:
            - answer (str): LLM generated answer
            - context (list[str]): Retrieved chunks used for generation
    """

    # Step 1: Retrieve relevant chunks from vector database
    # This is the "Retrieval" part of RAG
    chunks = retrieve_chunks(question)

    # Step 2: Handle empty retrieval case (Guardrail)
    # If no relevant chunks are found, we avoid calling the LLM
    if not chunks:
        return {
            "answer": "I could not find any relevant information in the document.",
            "context": []
        }

    # Step 3: Build prompt using question + retrieved chunks
    prompt = build_prompt(question, chunks)

    # Step 4: Call Groq LLM
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # updated from decommissioned llama3-8b-8192
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,  # low temperature = more factual, less creative
    )

    # Step 5: Extract answer from response
    answer = response.choices[0].message.content.strip()

    return {
        "answer": answer,
        "context": chunks
    }