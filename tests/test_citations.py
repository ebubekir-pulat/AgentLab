from agentlab.citations import validate_citations
from agentlab.retrieval import Passage


def test_all_citations_exist():
    passages = [
        Passage(source_id="source-a", text="First passage.", score=0.8),
        Passage(source_id="source-b", text="Second passage.", score=0.6),
    ]

    result = validate_citations(["source-a", "source-b"], passages)

    assert result.valid is True
    assert result.missing_source_ids == []


def test_missing_citation_is_reported():
    passages = [
        Passage(source_id="source-a", text="First passage.", score=0.8),
    ]

    result = validate_citations(["source-a", "source-missing"], passages)

    assert result.valid is False
    assert result.missing_source_ids == ["source-missing"]


def test_duplicate_citations_do_not_create_duplicate_errors():
    passages = [
        Passage(source_id="source-a", text="First passage.", score=0.8),
    ]

    result = validate_citations(
        ["source-missing", "source-missing"],
        passages,
    )

    assert result.valid is False
    assert result.missing_source_ids == ["source-missing"]


def test_no_citations_is_valid():
    result = validate_citations([], [])

    assert result.valid is True
    assert result.missing_source_ids == []