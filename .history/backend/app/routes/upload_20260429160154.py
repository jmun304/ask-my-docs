from fastapi import APIRouter, UploadFile, File
from app.services.pdf_utils import extract_pdf_text

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    result = await extract_pdf_text(file)

    return result
