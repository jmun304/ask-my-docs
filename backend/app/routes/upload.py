from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.pdf_utils import extract_pdf_text
from app.services.preprocessing import chunk_text
from app.services.vector_store import store_chunks, collection
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a PDF, extracts and chunks the text, and stores it in ChromaDB.
    Returns 400 if the file has already been uploaded, otherwise returns
    file_name, total_pages, num_chunks, and doc_id on success.
    """
    
    existing = collection.get(where={"file_name": file.filename})
    #print("existing:", existing) - for debugging
    #all_data = collection.get()
    #print(all_data['metadatas'])
    if existing and existing["ids"]:
        return JSONResponse(
            status_code=400,
            content={"error": f"{file.filename} has already been uploaded."}
        )
    
    result = await extract_pdf_text(file)
    num_chunks, chunks = chunk_text(result["full_text"]) #split into ~300 words piece
    doc_id = str(uuid.uuid4()) #generate random unique ID for the doc
    store_chunks(chunks, doc_id, file.filename) #save to ChromaDB
    return {
        "file_name": result["file_name"],
        "total_pages": result["total_pages"],
        "num_chunks": num_chunks,
        "doc_id": doc_id
    }