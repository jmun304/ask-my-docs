import pytest
import chromadb
from unittest.mock import patch
import backend.app.services.vector_store as vs
from backend.app.services.vector_store import store_chunks, query_chunks


# Fake embeddings - they just need to be the right dimensions / shape (i.e. list of lists of floats)
def fake_embeddings(texts: list[str]) -> list[list[float]]:
    return [[0.1, 0.2, 0.3] for _ in texts]


@pytest.fixture
def fake_collection():
    fake_client = chromadb.EphemeralClient()  # to create collection in-memory instead of on disk
    try:
        fake_client.delete_collection("docs")  # empty it for each test if it already exists
    except Exception:  # if it already doesn't exist yet
        pass
    return fake_client.get_or_create_collection(name="docs")


# ------------ store_chunks() tests ------------

@patch("backend.app.services.vector_store.embed_chunks", side_effect=fake_embeddings)
def test_store_chunks_creates_correct_ids(mock_embeddings, fake_collection):
    vs.collection = fake_collection
    store_chunks(["chunk one", "chunk two"], doc_id="doc123")

    # verify correct doc_ids were created
    results = fake_collection.get()
    assert "doc123_0" in results["ids"]
    assert "doc123_1" in results["ids"]


@patch("backend.app.services.vector_store.embed_chunks", side_effect=fake_embeddings)
def test_store_chunks_attaches_correct_metadata(mock_embeddings, fake_collection):
    vs.collection = fake_collection
    store_chunks(["chunk one", "chunk two"], doc_id="doc123")

    results = fake_collection.get()
    assert all(item["doc_id"] == "doc123" for item in results["metadatas"])


@patch("backend.app.services.vector_store.embed_chunks", side_effect=fake_embeddings)
def test_store_chunks_stores_correct_number_of_chunks(mock_embeddings, fake_collection):
    vs.collection = fake_collection
    store_chunks(["chunk one", "chunk two", "chunk three", "chunk four"], doc_id="doc123")

    results = fake_collection.get()
    assert len(results["ids"]) == 4


# ------------ query_chunks() tests ------------

@patch("backend.app.services.vector_store.embed_chunks", side_effect=fake_embeddings)
def test_query_chunks_returns_nonempty_results(mock_embeddings, fake_collection):
    vs.collection = fake_collection

    store_chunks(["A female rabbit is called a doe.", "A male rabbit is called a buck.",
                  "A baby rabbit is called a kit.", "A rabbit's parents are known as the dam (mother) and the sire (father)."],
                 doc_id="rabbits_doc")

    results = query_chunks(query="What is a baby rabbit called?", doc_id="rabbits_doc", n_results=1)

    assert len(results) > 0


@patch("backend.app.services.vector_store.embed_chunks", side_effect=fake_embeddings)
def test_query_chunks_filters_results_by_doc_correctly(mock_embeddings, fake_collection):
    vs.collection = fake_collection

    store_chunks(["A female rabbit is called a doe.", "A male rabbit is called a buck.",
                  "A baby rabbit is called a kit."], doc_id="rabbits_doc")
    store_chunks(["Baby animals often have special names.", "A baby deer is called a fawn.",
                  "A baby goose is called a gosling.", "A baby sugar glider is called a joey."],
                  doc_id="baby_animals")

    results = query_chunks(query="What is a baby goose called?", doc_id="baby_animals", n_results=1)
    assert "rabbit" not in results[0].lower()
    assert "gosling" in results[0].lower()


@patch("backend.app.services.vector_store.embed_chunks", side_effect=fake_embeddings)
def test_query_chunks_returns_empty_list_when_doc_id_does_not_exist(mock_embeddings, fake_collection):
    vs.collection = fake_collection

    store_chunks(["A female rabbit is called a doe.", "A male rabbit is called a buck.",
                  "A baby rabbit is called a kit."], doc_id="rabbits_doc")

    results = query_chunks(query="What is a baby goose called?", doc_id="baby_animals", n_results=1)
    assert results == []

