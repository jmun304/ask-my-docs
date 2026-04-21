from fastapi import FastAPI, UploadFile, File
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Backend is running!"}


# Upload endpoint (for PDFs)
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "message": "File received successfully (processing not implemented yet)"
    }


# Query endpoint (for questions)
@app.post("/query")
async def query_llm(question: str):
    return {
        "question": question,
        "answer": "This is a placeholder response (LLM not connected yet)"
    }
