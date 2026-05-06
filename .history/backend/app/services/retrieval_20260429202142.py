from app.services.vector_store import query_chunks

def retrieve_chunks(question: str, n_results: int = 5) -> list[str]:
    return query_chunks(question, n_results)