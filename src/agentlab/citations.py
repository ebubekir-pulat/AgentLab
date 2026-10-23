from dataclasses import dataclass

from agentlab.retrieval import Passage

@dataclass(frozen=True)
class CitationCheck:
    valid: bool
    missing_source_ids: list[str]


def validate_citations(
    cited_source_ids: list[str],
    available_passages: list[Passage],
) -> CitationCheck:
    """Check that every cited source ID appears in the available passages."""
    available_ids = {passage.source_id for passage in available_passages}
    cited_ids = set(cited_source_ids)

    missing_ids = sorted(cited_ids - available_ids)

    return CitationCheck(
        valid=not missing_ids,
        missing_source_ids=missing_ids,
    )