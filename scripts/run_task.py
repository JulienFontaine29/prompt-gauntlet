import argparse, json
from pathlib import Path
from llm_client import chat_completion_messages


def list_to_sentences(text: str) -> str:
    """Convert list-like text into smooth sentences with line breaks."""
    lines = [l.strip("-•* ") for l in text.splitlines() if l.strip()]
    if len(lines) <= 1:
        return text  # nothing to rewrite
    sentences = []
    for line in lines:
        if not line:
            continue
        # Capitalize first letter, ensure sentence ends with period
        s = line[0].upper() + line[1:]
        if not s.endswith((".", "?", "!")):
            s += "."
        sentences.append(s)
    # Join sentences with line breaks instead of spaces
    return "\n".join(sentences)


def postprocess(parsed):
    """Apply sentence-style formatting with line breaks to known fields."""
    if isinstance(parsed, dict):
        for key in ("summary", "actions", "risks", "red_flags"):
            if key in parsed and isinstance(parsed[key], str):
                parsed[key] = list_to_sentences(parsed[key])
    return parsed


def main():
    p = argparse.ArgumentParser(description="Run a Prompt Gauntlet task")
    p.add_argument("task_file", help="Path to task .txt")
    p.add_argument("--spec", default="prompts/prompt_spec.md", help="Prompt spec (Markdown) path")
    p.add_argument("--out", default=None, help="Output JSON/text path")
    args = p.parse_args()

    # Load spec + task
    spec_text = Path(args.spec).read_text()
    task_text = Path(args.task_file).read_text()

    # Always let the model decide based on the spec
    user = (
        "Task:\n" + task_text.strip() + "\n\n"
        "Follow the output_contract strictly. If JSON required, return ONLY JSON.\n"
    )

    content = chat_completion_messages(spec_text, user, temperature=0.2).strip()

    # Try to pretty-print JSON if valid
    try:
        parsed = json.loads(content)
        parsed = postprocess(parsed)  # format list-y fields
        content = json.dumps(parsed, indent=2, ensure_ascii=False)
    except Exception:
        # If it's not valid JSON, still try to make sentences with line breaks
        content = list_to_sentences(content)

    # Save or print
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(content)
    else:
        print(content)


if __name__ == "__main__":
    main()
