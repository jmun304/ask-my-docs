import chromadb
from app.core.config import CHROMA_DB_DIR, COLLECTION_NAME

from app.services.embedding import embed_text, embed_chunks

client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

collection = client.get_or_create_collection(name=COLLECTION_NAME)


def reset_collection():
    """
    Deletes old collection and recreates it.
    Used when uploading a new PDF.
    """

    global collection

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(name=COLLECTION_NAME)


def store_chunks(chunks: list[str]):
    """
    Store chunks in ChromaDB.
    """

    embeddings = embed_chunks(chunks)

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

    # Debug print-outs below
    print("DEBUG CHUNKS TYPE:", type(chunks))
    print("DEBUG SAMPLE:", chunks[:3])


def query_chunks(query: str, n_results: int = 3) -> list[str]:
    """
    Retrieve relevant chunks from ChromaDB.
    """

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results["documents"][0] if results["documents"] else []
