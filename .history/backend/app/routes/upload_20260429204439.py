from fastapi import APIRouter, UploadFile, File
from app.services.pdf_utils import extract_pdf_text
from app.services.preprocessing import chunk_text
from app.services.vector_store import store_chunks
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    result = await extract_pdf_text(file)
    num_chunks, chunks = chunk_text(result["full_text"]) #split into ~300 words piece
    doc_id = str(uuid.uuid4()) #generate random unique ID for the doc
    store_chunks(chunks, doc_id) #save to ChromaDB
    return {
        "filename": result["filename"],
        "total_pages": result["total_pages"],
        "num_chunks": num_chunks,
        "doc_id": doc_id
    }