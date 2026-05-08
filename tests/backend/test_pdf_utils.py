from backend.app.services.pdf_utils import extract_pdf_text
import pytest
from unittest.mock import MagicMock, AsyncMock
from fpdf import FPDF


def make_pdf_bytes(pages: list[str]) -> bytes:
    """Creates an in-memory PDF with one page per string in the list; returns the PDF as bytes"""
    pdf = FPDF()
    for page_text in pages:
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.cell(text=page_text)
    return bytes(pdf.output())


def make_upload_file(pdf_bytes, filename="test.pdf"):
    """Creates a mock FastAPI UploadFile object with the given PDF bytes and filename"""
    mock_file = MagicMock()
    mock_file.filename = filename
    mock_file.read = AsyncMock(return_value=pdf_bytes)
    return mock_file


def make_example_upload_file_1():
    """Creates a specific mock file for testing"""
    pdf_bytes = make_pdf_bytes(["test page 1", "test page 2"])
    example_file = make_upload_file(pdf_bytes, filename="testfile1.pdf")
    return example_file


@pytest.fixture
def real_pdf_bytes_python_wikipedia():
    # open pdf in binary format for reading
    with open("tests/backend/fixtures/Python (programming language) - Wikipedia.pdf", "rb") as f:
        return f.read()


# ------------ Test Cases ------------

@pytest.mark.asyncio
async def test_mock_file_extract_pdf_text_returns_full_text():
    """Creates a mock UploadFile and checks that extract_pdf_text() correctly returns all pages' text"""
    mock_file = make_example_upload_file_1()
    result = await extract_pdf_text(mock_file)
    assert "test page 1" in result["full_text"]
    assert "test page 2" in result["full_text"]


@pytest.mark.asyncio
async def test_mock_file_extract_pdf_text_returns_correct_filename():
    """Creates a mock UploadFile and checks that extract_pdf_text() returns correct filename"""
    mock_file = make_example_upload_file_1()
    result = await extract_pdf_text(mock_file)
    assert result["filename"] == "testfile1.pdf"


@pytest.mark.asyncio
async def test_mock_file_extract_pdf_text_returns_correct_preview():
    """Creates a mock UploadFile and checks that extract_pdf_text() returns correct preview"""
    mock_file = make_example_upload_file_1()
    result = await extract_pdf_text(mock_file)
    assert result["preview"] == result["full_text"][:1000]


@pytest.mark.asyncio
async def test_mock_file_extract_pdf_text_returns_correct_total_pages():
    """Creates a mock UploadFile and checks that extract_pdf_text() returns correct number of total pages"""
    mock_file = make_example_upload_file_1()
    result = await extract_pdf_text(mock_file)
    assert result["total_pages"] == 2


@pytest.mark.asyncio
async def test_real_file_extract_pdf_text_full_text(real_pdf_bytes_python_wikipedia):
    """Creates an UploadFile from real pdf and checks that extract_pdf_text() returns correct full text"""
    test_file = make_upload_file(real_pdf_bytes_python_wikipedia, filename="python-wikipedia.pdf")
    result = await extract_pdf_text(test_file)
    # make sure the full_text is a non-empty string and contains key phrases from pdf
    assert isinstance(result["full_text"], str)
    assert len(result["full_text"]) > 0
    assert "Guido van Rossum" in result["full_text"]
    assert "Zen of Python" in result["full_text"]
    assert "whitespace indentation" in result["full_text"]


@pytest.mark.asyncio
async def test_real_file_extract_pdf_text_returns_correct_preview(real_pdf_bytes_python_wikipedia):
    """Creates an UploadFile from real pdf and checks that extract_pdf_text() returns correct preview"""
    test_file = make_upload_file(real_pdf_bytes_python_wikipedia, filename="python-wikipedia.pdf")
    result = await extract_pdf_text(test_file)
    assert result["preview"] == result["full_text"][:1000]


@pytest.mark.asyncio
async def test_real_file_extract_pdf_text_returns_correct_total_pages(real_pdf_bytes_python_wikipedia):
    """Creates an UploadFile from real pdf and checks that extract_pdf_text() returns correct total number of pages"""
    test_file = make_upload_file(real_pdf_bytes_python_wikipedia, filename="python-wikipedia.pdf")
    result = await extract_pdf_text(test_file)
    assert result["total_pages"] == 37
