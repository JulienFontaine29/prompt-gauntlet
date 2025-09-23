import argparse, json, re
from pathlib import Path
from llm_client import chat_completion_messages


def is_prompt_empty(spec_text: str) -> bool:
    """
    True if all editable sections are still placeholders ('-' or blank).
    """
    sections = [
        "## Objective",
        "## Audience",
        "## Role Persona",
        "## Scope",
        "## Style Guide",
        "## Context",
        "## Guardrails"
    ]
    for section in sections:
        m = re.search(rf"{section}\n(.*?)(?=\n##|\Z)", spec_text, re.DOTALL)
        if not m:
            continue
        content = m.group(1).strip()
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        if any(l not in ("-", "–", "—") for l in lines):
            return False
    return True


def is_prompt_weak(spec_text: str) -> bool:
    """
    True if spec technically has content but it's trivial (very few chars).
    """
    filled_chars = 0
    sections = [
        "## Objective", "## Audience", "## Role Persona",
        "## Scope", "## Style Guide", "## Context", "## Guardrails"
    ]
    for section in sections:
        m = re.search(rf"{section}\n(.*?)(?=\n##|\Z)", spec_text, re.DOTALL)
        if not m:
            continue
        content = m.group(1).strip().replace("-", "")
        filled_chars += len(content)
    return filled_chars < 30  # adjust threshold as needed


def list_to_sentences(text: str) -> str:
    lines = [l.strip("-•* ") for l in text.splitlines() if l.strip()]
    if len(lines) <= 1:
        return text
    sentences = []
    for line in lines:
        s = line[0].upper() + line[1:]
        if not s.endswith((".", "?", "!")):
            s += "."
        sentences.append(s)
    return "\n".join(sentences)


def postprocess(parsed):
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

    spec_text = Path(args.spec).read_text()
    task_text = Path(args.task_file).read_text()

    # --- Empty prompt guard ---
    if is_prompt_empty(spec_text):
        print(json.dumps({
            "error": "Prompt spec not filled in",
            "message": "The editable sections are still placeholders. Please fill them in."
        }, indent=2))
        return

    # --- Weak prompt guard ---
    if is_prompt_weak(spec_text):
        print(json.dumps({
            "error": "Prompt spec too weak",
            "message": "The spec contains only minimal filler. Please expand sections with real detail."
        }, indent=2))
        return

    # Run model with strict refusal rule
    system = (
        spec_text
        + "\n\nIMPORTANT: If the prompt spec is vague or incomplete, "
          "return this exact JSON instead of improvising:\n"
          '{ "summary": "Prompt spec incomplete — cannot generate meaningful output", '
          '"actions": [], "risks_or_redflags": [] }'
    )

    user = (
        "Task:\n" + task_text.strip() + "\n\n"
        "Follow the output_contract strictly. If JSON required, return ONLY JSON.\n"
    )

    content = chat_completion_messages(system, user, temperature=0.2).strip()

    try:
        parsed = json.loads(content)
        parsed = postprocess(parsed)
        content = json.dumps(parsed, indent=2, ensure_ascii=False)
    except Exception:
        content = list_to_sentences(content)

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(content)
    else:
        print(content)


if __name__ == "__main__":
    main()
