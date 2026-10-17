from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    """A normalised source document."""
    source_id: str
    text: str


def ingest_text(text: str, source_id: str) -> Document:
    """Normalise text and create a document with a source ID."""
    if not text.strip():
        raise ValueError("Document text must not be empty")

    normalised = " ".join(text.split())

    if not source_id.strip():
        raise ValueError("source_id must not be empty")

    return Document(source_id=source_id, text=normalised)


def ingest_file(path: str | Path, source_id: str | None = None) -> Document:
    """Read a UTF-8 text file and ingest its contents."""
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    resolved_source_id = source_id or file_path.name

    return ingest_text(text, resolved_source_id)
