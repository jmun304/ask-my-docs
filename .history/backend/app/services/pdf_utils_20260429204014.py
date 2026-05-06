import io
import PyPDF2
from app.services.preprocessing import clean_text


async def extract_pdf_text(file):
    # Read file bytes from upload
    contents = await file.read()

    # Parse PDF using PyPDF2
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))

    # Extract text from all pages
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    # Clean extracted text
    text = clean_text(text)

    return {
        "filename": file.filename,
        "full_text": text, #return full text
        "preview": text[:1000],
        "total_pages": len(pdf_reader.pages)
    }
