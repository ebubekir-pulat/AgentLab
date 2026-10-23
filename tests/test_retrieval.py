import pytest

from agentlab.ingestion import ingest_text
from agentlab.retrieval import retrieve

@pytest.fixture
def documents():
    return [
        ingest_text(
            "Local language models can run without cloud services. "
            "They can improve privacy by keeping data on-device.",
            "local-models",
        ),
        ingest_text(
            "Citation validation checks whether referenced sources exist. "
            "It does not prove that a claim is factually correct.",
            "citations",
        ),
        ingest_text(
            "Automated tests catch regressions in software.",
            "testing",
        ),
    ]


def test_retrieve_returns_relevant_passage_first(documents):
    results = retrieve("local models privacy", documents, top_k=3)
    
    assert results
    assert results[0].source_id == "local-models"
    assert "local language models" in results[0].text.lower()


def test_retrieve_preserves_source_ids(documents):
    results = retrieve("citation sources", documents)

    assert results
    assert all(result.source_id == "citations" for result in results)


def test_retrieve_returns_no_results_for_unmatched_query(documents):
    results = retrieve("volcano astronomy", documents)

    assert results == []


def test_retrieve_rejects_invalid_top_k(documents):
    with pytest.raises(ValueError, match="top_k must be at least 1"):
        retrieve("local models", documents, top_k=0)


def test_retrieve_respects_top_k(documents):
    results = retrieve("local models citation tests", documents, top_k=2)

    assert len(results) <= 2