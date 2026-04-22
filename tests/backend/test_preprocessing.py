# Testing clean_text() and chunk_text() functions
from backend.preprocessing import clean_text, chunk_text


# ------------ clean_text() tests ------------

def test_clean_text_removes_extra_spaces():
    result = clean_text(" this    is a   test  ")
    assert result == "this is a test"


def test_clean_text_preserves_paragraph_breaks():
    result = clean_text("Paragraph one.\n\nParagraph two.")
    assert "\n\n" in result


def test_clean_text_deletes_extra_newlines():
    result = clean_text("line one\n\n\nline two")
    assert "\n\n\n" not in result


def test_clean_text_handles_empty_string():
    result = clean_text("")
    assert result == ""


# ------------ chunk_text() texts ------------

def test_chunk_text_returns_multiple_chunks():
    num_chunks, chunks = chunk_text("word " * 1000)
    assert num_chunks > 1


def test_chunk_text_returns_correct_chunk_size():
    num_chunks, chunks = chunk_text("word " * 1000, chunk_size=300)
    word_count = len(chunks[0].split())
    assert word_count == 300
