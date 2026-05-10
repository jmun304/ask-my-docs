import pytest
import chromadb
from unittest.mock import patch

import backend.app.services.vector_store as vs
from backend.app.services.vector_store import store_chunks, query_chunks


# -------------------------------------------------
# Fake embeddings (deterministic but NOT identical)
# This avoids Chroma treating everything as equal
# -------------------------------------------------
def fake_embeddings(texts: list[str]) -> list[list[float]]:
    return [
        [
            float(len(text)),          # simple signal: length
            float("kit" in text),      # keyword signal
            float("rabbit" in text)    # keyword signal
        ]
        for text in texts
    ]


# -------------------------------------------------
# In-memory Chroma collection for testing
# -------------------------------------------------
@pytest.fixture
def fake_collection():
    client = chromadb.EphemeralClient()

    try:
        client.delete_collection("docs")
    except Exception:
        pass

    return client.get_or_create_collection(name="docs")


# -------------------------------------------------
# store_chunks tests
# -------------------------------------------------

@patch("backend.app.services.vector_store.embed_chunks", side_effect=fake_embeddings)
def test_store_chunks_creates_ids(mock_embed, fake_collection):
    vs.collection = fake_collection

    store_chunks(["chunk one", "chunk two"])

    results = fake_collection.get()

    assert "chunk_0" in results["ids"]
    assert "chunk_1" in results["ids"]


@patch("backend.app.services.vector_store.embed_chunks", side_effect=fake_embeddings)
def test_store_chunks_stores_all_documents(mock_embed, fake_collection):
    vs.collection = fake_collection

    chunks = ["a", "b", "c", "d"]
    store_chunks(chunks)

    results = fake_collection.get()

    assert len(results["documents"]) == 4
    assert results["documents"] == chunks


# -------------------------------------------------
# query_chunks tests
# -------------------------------------------------

@patch("backend.app.services.vector_store.embed_text", side_effect=lambda q: [len(q), 0.0, 0.0])
@patch("backend.app.services.vector_store.embed_chunks", side_effect=fake_embeddings)
def test_query_chunks_returns_list(mock_chunks, mock_query, fake_collection):
    vs.collection = fake_collection

    store_chunks([
        "A female rabbit is called a doe.",
        "A male rabbit is called a buck.",
        "A baby rabbit is called a kit.",
        "Rabbits are social animals."
    ])

    results = query_chunks(query="rabbit", n_results=2)

    assert isinstance(results, list)
    assert len(results) > 0


@patch("backend.app.services.vector_store.embed_text", side_effect=lambda q: [0.0, 0.0, 0.0])
@patch("backend.app.services.vector_store.embed_chunks", side_effect=fake_embeddings)
def test_query_chunks_returns_empty_when_no_data(mock_chunks, mock_query, fake_collection):
    vs.collection = fake_collection

    # no chunks stored
    results = query_chunks(query="anything", n_results=1)

    assert results == []


@patch("backend.app.services.vector_store.embed_text", side_effect=lambda q: [len(q), 1.0, 1.0])
@patch("backend.app.services.vector_store.embed_chunks", side_effect=fake_embeddings)
def test_query_chunks_returns_relevant_results(mock_chunks, mock_query, fake_collection):
    vs.collection = fake_collection

    store_chunks([
        "A female rabbit is called a doe.",
        "A male rabbit is called a buck.",
        "A baby rabbit is called a kit."
    ])

    results = query_chunks(query="baby rabbit", n_results=1)

    assert isinstance(results, list)
    assert len(results) > 0
    assert "rabbit" in results[0].lower()