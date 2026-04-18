from fastapi import FastAPI, UploadFile, File
import PyPDF2
import io

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

# Accept PDF upload and extract text
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):   
    # Read file bytes from upload
    contents = await file.read()
    
    # Parse PDF using PyPDF2
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))
    
    # Extract text from all pages
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    return {
        "filename": file.filename,
        "preview": text[:1000],
        "total_pages": len(pdf_reader.pages)
    }

@app.post("/query")
async def query_llm(question: str):
    return {
        "question": question,
        "answer": "This is a placeholder response (LLM not connected yet)"
    }