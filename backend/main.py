from fastapi import FastAPI, UploadFile, File
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:
    """Removes extra newline characters and extra spaces from text; Returns cleaned text"""
    # Remove leading and trailing spaces
    text = text.strip()
    # replace spaces longer than 1 character (or tabs) with a single space
    text = re.sub(r"[ \t]+", " ", text)
    # replace any instances of 3+ newline characters with 2 newline characters
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


def chunk_text(text: str, chunk_size: int = 300) -> tuple[int, list[str]]:
    """Splits given text into chunks of given chunk_size (default is 300 words); Returns number of chunks and a list of
    the chunks as strings"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0, length_function=lambda t:
    len(t.split()), is_separator_regex=False)

    chunks = text_splitter.split_text(text=text)  # returns a list of the chunks as strings

    return len(chunks), chunks


def get_preview_of_chunk(chunk: str, num_words: int = 10) -> str:
    """Returns the first num_words words of the given chunk as a string"""
    word_list = chunk.split()
    return " ".join(word_list[:num_words])


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
