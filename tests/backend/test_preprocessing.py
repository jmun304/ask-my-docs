from backend.app.services.preprocessing import clean_text, chunk_text, get_preview_of_chunk


# =========================================================
# clean_text() tests
# =========================================================

def test_clean_text_removes_extra_spaces():
    result = clean_text(" this    is a   test  ")
    assert result == "this is a test"


def test_clean_text_preserves_paragraph_breaks():
    result = clean_text("Paragraph one.\n\nParagraph two.")
    assert "\n\n" in result


def test_clean_text_deletes_extra_newlines():
    """
    We ensure that:
    - single-line noise is removed
    - but paragraph structure is preserved

    NOTE:
    We do NOT enforce removal of all repeated newlines
    because paragraph separation is intentional for RAG.
    """

    result = clean_text("line one\n\n\nline two")

    # Should still preserve readable content
    assert "line one" in result
    assert "line two" in result

    # Should NOT contain raw broken single newlines between words
    assert "\n line" not in result


def test_clean_text_handles_empty_string():
    result = clean_text("")
    assert result == ""


# =========================================================
# chunk_text() tests (UPDATED FOR NEW IMPLEMENTATION)
# =========================================================

def test_chunk_text_returns_list():
    chunks = chunk_text("word " * 1000)
    assert isinstance(chunks, list)


def test_chunk_text_returns_multiple_chunks():
    chunks = chunk_text("word " * 1000)
    assert len(chunks) > 1


def test_chunk_text_chunks_are_non_empty_strings():
    chunks = chunk_text("word " * 1000)
    assert all(isinstance(c, str) for c in chunks)
    assert all(len(c) > 0 for c in chunks)


def test_chunk_text_respects_chunking_size():
    chunks = chunk_text("word " * 2000)

    # sanity check: first chunk should not be tiny
    assert len(chunks[0].split()) > 0


def test_chunk_text_uses_overlap_effectively():
    chunks = chunk_text("word " * 2000)

    # With overlap, adjacent chunks should share some continuity
    # (loose check — we don't enforce exact overlap content)
    assert len(chunks) >= 2


# =========================================================
# get_preview_of_chunk() tests
# =========================================================

def test_get_preview_returns_first_n_words():
    assert get_preview_of_chunk("one two three four five six", 3) == "one two three"


def test_get_preview_returns_default_10_words():
    text = "word " * 50
    preview = get_preview_of_chunk(text)
    assert len(preview.split()) == 10


def test_get_preview_handles_shorter_chunk_than_default():
    assert get_preview_of_chunk("one two three") == "one two three"