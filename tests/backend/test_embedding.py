from backend.app.services.embedding import embed_chunks, embed_text
from sklearn.metrics.pairwise import cosine_similarity


# ------------ embed_chunks() tests ------------

def test_embed_chunks_returns_list_of_lists():
    result = embed_chunks(["first string", "second string"])
    assert isinstance(result, list)
    assert all(isinstance(sublist, list) for sublist in result)


def test_embed_chunks_returns_floats_in_lists():
    result = embed_chunks(["first string", "second_string"])
    assert all(isinstance(x, float) for sublist in result for x in sublist)


def test_embed_chunks_correct_dimensions():
    result = embed_chunks(["first string", "second string", "third string"])
    assert len(result) == 3
    assert all(len(sublist) == 384 for sublist in result)


def test_embed_chunks_same_inputs_same_results():
    chunks = ["kittens", "bunnies", "ducklings"]
    result1 = embed_chunks(chunks)
    result2 = embed_chunks(chunks)
    assert result1 == result2


def test_embed_chunks_cosine_similarity():
    """Semantically similar texts should have cosine similarity close to 1.
    No similarity should have cosine similarity closer to 0,
    and opposite meanings closer to -1."""
    results = embed_chunks(["rabbits", "bunnies", "squirrels"])
    similarity_related = cosine_similarity([results[0]], [results[1]])
    similarity_unrelated = cosine_similarity([results[0]], [results[2]])
    assert similarity_related > similarity_unrelated


# ------------ embed_text() tests ------------

def test_embed_text_returns_list():
    result = embed_text("sample text")
    assert isinstance(result, list)


def test_embed_text_returns_floats_in_list():
    result = embed_text("sample text")
    assert all(isinstance(x, float) for x in result)


def test_embed_text_correct_dimension():
    result = embed_text("sample text")
    assert len(result) == 384  # all-MiniLM-L6-v2 output dimension


def test_embed_text_same_inputs_same_results():
    result1 = embed_text("This is a sentence.")
    result2 = embed_text("This is a sentence.")
    assert result1 == result2


def test_embed_text_different_inputs_different_results():
    result1 = embed_text("Who doesn't love kittens?")
    result2 = embed_text("quantum computing")
    assert result1 != result2


def test_embed_text_empty_string():
    result = embed_text("")
    assert isinstance(result, list)
    assert len(result) == 384


def test_embed_text_long_string():
    long_string = "word " * 1000
    result = embed_text(long_string)
    assert isinstance(result, list)
    assert len(result) == 384
