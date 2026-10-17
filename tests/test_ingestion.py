import pytest

from agentlab.ingestion import Document, ingest_file, ingest_text


def test_ingest_text_normalises_whitespace():
    document = ingest_text(
        "  Reliable   AI\n agents\tneed evidence.  ",
        "source-1",
    )

    assert document == Document(
        source_id="source-1",
        text="Reliable AI agents need evidence.",
    )


def test_ingest_text_rejects_empty_text():
    with pytest.raises(ValueError, match="Document text must not be empty"):
        ingest_text(" \n\t ", "source-1")


def test_ingest_text_rejects_empty_source_id():
    with pytest.raises(ValueError, match="source_id must not be empty"):
        ingest_text("Some useful content.", "  ")


def test_ingest_file_reads_utf8_text(tmp_path):
    path = tmp_path / "source.txt"
    path.write_text("First line.\nSecond line.", encoding="utf-8")

    document = ingest_file(path, source_id="paper-1")

    assert document.source_id == "paper-1"
    assert document.text == "First line. Second line."


def test_ingest_file_defaults_source_id_to_filename(tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("Some research notes.", encoding="utf-8")

    document = ingest_file(path)

    assert document.source_id == "notes.txt"
    assert document.text == "Some research notes."