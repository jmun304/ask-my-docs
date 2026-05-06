import chromadb

client = chromadb.PersistentClient(path="./data/chroma") #ChromaDB's default embeddings
collection = client.get_or_create_collection(name="docs")

#builds unique ID for every chunk in a pdf and then stores them in vectors
def store_chunks(chunks: list[str], doc_id: str): 
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids)

#
def query_chunks(query: str, n_results: int = 5) -> list[str]: 
    results = collection.query(query_texts=[query], n_results=n_results)
    return results["documents"][0] if results["documents"] else []