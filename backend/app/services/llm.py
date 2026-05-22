from ollama import chat, ChatResponse


def build_prompt(question: str, context: list[str]) -> str:
    """
    Creates an LLM prompt with the user question and the retrieved chunks (context).
    """
    context = "\n".join(context)
    return f"""You're a helpful RAG assistant. Answer the following question using only the given context.
    If the answer is not in the given context, just say, 'I don't have enough information to answer that based on the document.'
    Do not use information from training data or other outside information that is not in the given context.
    
    Context: 
    {context}
    
    Question: 
    {question}
    
    Answer:"""


def generate_response(prompt: str) -> str:
    """
    Designates a local LLM and prompts it with the given prompt.
    Returns the LLM's answer as a string, or if no answer received, returns empty string.
    Usage taken from Ollama python documentation: https://github.com/ollama/ollama-python
    """
    response: ChatResponse = chat(
        model='mistral',
        messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ]
    )
    return response.message.content or ""
