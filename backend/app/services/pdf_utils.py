from pypdf import PdfReader


def extract_pdf_text(file) -> str:
    """
    Extract raw text from uploaded PDF using pypdf.

    IMPORTANT NOTES:
    - This returns RAW text (still messy by nature of PDFs)
    - DO NOT try to over-clean here
    - Keep structure (pages) so downstream chunking works better
    """

    reader = PdfReader(file.file)

    pages_text = []

    for page in reader.pages:
        # extract_text() may return None for image-based or weird PDFs
        page_text = page.extract_text() or ""

        # Keep page separation to preserve structure
        pages_text.append(page_text)

    # Join pages with clear separation: this prevents word-splitting across page boundaries
    text = "\n\n".join(pages_text)

    return text
