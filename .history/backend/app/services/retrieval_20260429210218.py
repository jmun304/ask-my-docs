from app.services.vector_store import query_chunks

def retrieve_chunks(question: str, doc_id: str = None, n_results: int = 5) -> list[str]:
    return query_chunks(question, doc_id, n_results)