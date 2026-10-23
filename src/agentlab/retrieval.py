import re
from dataclasses import dataclass

from agentlab.ingestion import Document

def tokenise(text: str) -> set[str]:
    """Return lowercase word tokens."""
    return set(re.findall(r"\b\w+\b", text.lower()))


@dataclass(frozen=True)
class Passage:
    source_id: str
    text: str
    score: float


def retrieve(
    query: str,
    documents: list[Document],
    top_k: int = 5,
) -> list[Passage]:
    """Retrieve passages ranked by lexical overlap with the query."""
    
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    query_tokens = tokenise(query)
    if not query_tokens:
        return []

    candidates: list[Passage] = []

    for document in documents:
        # Ingestion already normalises whitespace
        sentences = re.split(r"(?<=[.!?])\s+", document.text)

        for sentence in sentences:
            text = sentence.strip()
            if not text:
                continue

            passage_tokens = tokenise(text)
            if not passage_tokens:
                continue

            overlap = query_tokens & passage_tokens
            if not overlap:
                continue

            # Jaccard similarity gives a score between 0 and 1
            score = len(overlap) / len(query_tokens | passage_tokens)

            candidates.append(
                Passage(
                    source_id=document.source_id,
                    text=text,
                    score=score,
                )
            )

    # Stable tie-breaking makes retrieval deterministic.
    candidates.sort(key=lambda p: (-p.score, p.source_id, p.text))

    return candidates[:min(top_k, len(candidates))]