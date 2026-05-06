import chromadb

client = chromadb.PersistentClient(path="./data/chroma") #ChromaDB's default embeddings
collection = client.get_or_create_collection(name="docs")

# Isolate queries by doc_id
# Builds unique ID for every chunk in a pdf and then stores them in vectors
def store_chunks(chunks: list[str], doc_id: str):
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
    metadatas = [{"doc_id": doc_id} for _ in chunks]
    collection.add(documents=chunks, ids=ids, metadatas=metadatas)

# Convert query into vector and return 5 relevant chunks
def query_chunks(query: str, doc_id: str = None, n_results: int = 5) -> list[str]:
    where = {"doc_id": doc_id} if doc_id else None
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where
    )
    return results["documents"][0] if results["documents"] else []