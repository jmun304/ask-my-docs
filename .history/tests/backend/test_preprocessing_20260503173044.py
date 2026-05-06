# Testing clean_text() and chunk_text() functions
from backend.app.services.preprocessing import clean_text, chunk_text, get_preview_of_chunk


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

def test_chunk_text_returns_correct_types():
    num_chunks, chunks = chunk_text("word " * 1000)
    assert isinstance(num_chunks, int)
    assert isinstance(chunks, list)


def test_chunk_text_returns_multiple_chunks():
    num_chunks, chunks = chunk_text("word " * 1000)
    assert num_chunks > 1


def test_chunk_text_returns_correct_default_chunk_size():
    num_chunks, chunks = chunk_text("word " * 1000)
    word_count = len(chunks[0].split())
    assert word_count == 300


def test_chunk_text_returns_correct_specified_chunk_size():
    num_chunks, chunks = chunk_text("word " * 1000, 100)
    word_count = len(chunks[0].split())
    assert word_count == 100


# ------------ get_preview_of_chunk() tests ------------

def test_get_preview_returns_first_n_words():
    assert get_preview_of_chunk("one two three four five six", 3) == "one two three"


def test_get_preview_returns_default_10_words():
    text = "word " * 50
    preview = get_preview_of_chunk(text)
    assert len(preview.split()) == 10


def test_get_preview_handles_shorter_chunk_than_default():
    assert get_preview_of_chunk("one two three") == "one two three"
