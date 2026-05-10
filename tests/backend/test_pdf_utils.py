from backend.app.services.pdf_utils import extract_pdf_text
import pytest
from unittest.mock import MagicMock
from fpdf import FPDF
import io
import os


# ----------------------------
# Test Helpers
# ----------------------------

def make_pdf_bytes(pages: list[str]) -> bytes:
    """
    Creates an in-memory PDF for testing purposes.

    Each string in `pages` becomes a separate PDF page.

    WHY THIS EXISTS:
    - Avoids needing real files on disk
    - Lets us simulate multi-page PDFs
    - Keeps tests fast + deterministic
    """
    pdf = FPDF()

    for page_text in pages:
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)

        # Adds simple text content to page
        pdf.cell(text=page_text)

    return bytes(pdf.output())


def make_upload_file(pdf_bytes, filename="test.pdf"):
    """
    Creates a mock object that behaves like FastAPI's UploadFile.

    KEY FIX:
    - pypdf requires a real file-like object
    - so we use io.BytesIO instead of MagicMock streams
    """
    mock_file = MagicMock()
    mock_file.filename = filename

    # REAL file-like object (fixes pypdf crash)
    mock_file.file = io.BytesIO(pdf_bytes)

    return mock_file


def make_example_upload_file_1():
    """
    Standard test PDF:
    - 2 pages
    - predictable content for assertions
    """
    pdf_bytes = make_pdf_bytes(["test page 1", "test page 2"])
    return make_upload_file(pdf_bytes, filename="testfile1.pdf")


# ----------------------------
# Fixtures
# ----------------------------

@pytest.fixture
def real_pdf_bytes_python_wikipedia():
    """
    Loads a real PDF from disk for integration testing.

    This ensures pipeline works on real-world PDFs.
    """
    path = os.path.join(
        os.path.dirname(__file__),
        "fixtures",
        "Python (programming language) - Wikipedia.pdf"
    )

    with open(path, "rb") as f:
        return f.read()


# ----------------------------
# Mock PDF Tests
# ----------------------------

def test_mock_file_extract_pdf_text_returns_full_text():
    """
    Ensures:
    - all pages are extracted
    - returned value is a single combined string
    """
    mock_file = make_example_upload_file_1()
    result = extract_pdf_text(mock_file)

    assert isinstance(result, str)
    assert "test page 1" in result
    assert "test page 2" in result


def test_mock_file_extract_pdf_text_is_string():
    """
    Basic sanity check:
    extraction should always return a string
    """
    mock_file = make_example_upload_file_1()
    result = extract_pdf_text(mock_file)

    assert isinstance(result, str)


# ----------------------------
# Real PDF Tests
# ----------------------------

def test_real_file_extract_pdf_text_full_content(real_pdf_bytes_python_wikipedia):
    """
    Ensures real-world PDF extraction works correctly.

    We validate known phrases from Wikipedia Python article.
    """
    test_file = make_upload_file(
        real_pdf_bytes_python_wikipedia,
        filename="python-wikipedia.pdf"
    )

    result = extract_pdf_text(test_file)

    assert isinstance(result, str)
    assert len(result) > 0

    # Key expected phrases
    assert "Guido van Rossum" in result
    assert "Zen of Python" in result
    assert "whitespace indentation" in result


def test_real_file_extract_pdf_text_is_string(real_pdf_bytes_python_wikipedia):
    """
    Sanity check:
    real PDF output must always be a string.
    """
    test_file = make_upload_file(
        real_pdf_bytes_python_wikipedia,
        filename="python-wikipedia.pdf"
    )

    result = extract_pdf_text(test_file)

    assert isinstance(result, str)