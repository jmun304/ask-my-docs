from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def embed_text(input_string: str) -> list[float]:
    """Converts a single string into embedding vector, i.e. a numpy array.
    Returns embedding vector as a python list"""
    embedding = model.encode(input_string)
    return embedding.tolist()   # convert numpy array to python list


def embed_chunks(input_chunks: list[str]) -> list[list[float]]:
    """Converts a list of strings (text chunks) into embedding vectors, i.e. a 2D numpy array.
    Returns them as a python list of lists"""
    embeddings = model.encode(input_chunks)
    return embeddings.tolist()

