from fastapi import APIRouter, UploadFile, File

from app.services.pdf_utils import extract_pdf_text
from app.services.preprocessing import clean_text, chunk_text
from app.services.vector_store import reset_collection, store_chunks

router = APIRouter()


@router.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    # 1. Extract text (ref: pdf_utils.py)
    text = extract_pdf_text(file)

    # 2. Clean text (ref: preprocessing.py)
    cleaned = clean_text(text)

    # 3. Chunk text (ref: preprocessing.py), MUST return list[str]
    chunks = chunk_text(cleaned)

    # 4. Reset vector DB (single PDF MVP rule) - wipes old embeddings (ref: vector_store.py)
    reset_collection()

    # 5. Store chunks (ref: vector_store.py)
    store_chunks(chunks)

    return {
        "message": "PDF processed successfully",
        "num_chunks": len(chunks)
    }