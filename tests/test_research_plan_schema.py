import json
from pathlib import Path

from jsonschema import validate, ValidationError
import pytest

ROOT = Path.cwd()
SCHEMA_PATH = ROOT / "schemas" / "research_plan.schema.json"

@pytest.fixture
def schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

def test_valid_research_plan_passes(schema):
    plan = {
        "topic": "Reliable local AI agents",
        "research_question": "How can local models support reliable agents?",
        "steps": [
            {"action": "Review literature", "purpose": "Understand prior work"},
            {"action": "Run experiments", "purpose": "Measure reliability"},
            {"action": "Evaluate results", "purpose": "Compare approaches"},
        ],
    }

    validate(instance=plan, schema=schema)

def test_research_plan_with_too_few_steps_fails(schema):
    plan = {
        "topic": "Reliable local AI agents",
        "research_question": "How can local models support reliable agents?",
        "steps": [
            {"action": "Review literature", "purpose": "Understand prior work"},
            {"action": "Run experiments", "purpose": "Measure reliability"},
        ],
    }

    with pytest.raises(ValidationError):
        validate(instance=plan, schema=schema)

def test_research_plan_with_missing_field_fails(schema):
    plan = {
        "topic": "Reliable local AI agents",
        "steps": [
            {"action": "Review literature", "purpose": "Understand prior work"},
            {"action": "Run experiments", "purpose": "Measure reliability"},
            {"action": "Evaluate results", "purpose": "Compare approaches"},
        ],
    }

    with pytest.raises(ValidationError):
        validate(instance=plan, schema=schema)