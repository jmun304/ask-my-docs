from app.services.vector_store import query_chunks
from app.core.config import TOP_K_RESULTS


def retrieve_chunks(question: str) -> list[str]:
    return query_chunks(
        query=question,
        n_results=TOP_K_RESULTS
    )
