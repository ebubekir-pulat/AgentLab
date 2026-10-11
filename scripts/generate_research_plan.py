import json
from pathlib import Path
from ollama import chat, ChatResponse
from jsonschema import validate

ROOT = Path.cwd()
SCHEMA_PATH = ROOT / "schemas" / "research_plan.schema.json"
OUTPUT_PATH = ROOT / "research_plan.json"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.1"

def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    print(f"Requesting a research plan from {MODEL}...")

    response: ChatResponse = chat(
        model = MODEL,
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a research planning assistant. "
                    "Create practical, specific research steps. "
                    "Return only JSON matching the requested schema."
                )
            },
            {
                "role": "user",
                "content": (
                    "Create a research plan for this question. "
                    "'How can local language models be used to build "
                    "reliable AI agents?' Include 3 to 5 actionable steps. "
                    "The required JSON schema is:\n"
                    + json.dumps(schema)
                )
            }
        ],
        format = schema,
        stream = False,
        options = {"temperature": 0},
    )

    plan = json.loads(response['message']['content'])

    validate(instance=plan, schema=schema)

    OUTPUT_PATH.write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("PASS: generated research plan satisfies the JSON Schema.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(json.dumps(plan, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()