import argparse, json, re
from pathlib import Path
from llm_client import chat_completion_messages


def is_prompt_empty(spec_text: str) -> bool:
    sections = [
        "## Objective", "## Audience", "## Role Persona",
        "## Scope", "## Style Guide", "## Context", "## Guardrails"
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
    return filled_chars < 30


def main():
    p = argparse.ArgumentParser(description="Judge a team submission")
    p.add_argument("candidate_json", help="Path to team’s model output JSON")
    p.add_argument("--task", required=True, help="Task file path")
    p.add_argument("--spec", default="prompts/prompt_spec.md", help="Team’s prompt spec file")
    p.add_argument("--context", required=True, help="Context file path")
    args = p.parse_args()

    rubric = Path("prompts/judge_prompt.txt").read_text()
    spec_text = Path(args.spec).read_text()
    task_text = Path(args.task).read_text()
    context_text = Path(args.context).read_text()
    model_output = Path(args.candidate_json).read_text()

    # --- Empty spec = auto 0 ---
    if is_prompt_empty(spec_text):
        print(json.dumps({
            "context": 0,
            "structure": 0,
            "scope": 0,
            "guardrails": 0,
            "style": 0,
            "safety": 0,
            "brevity": 0,
            "total": 0,
            "triggered_traps": ["Prompt spec not filled in"],
            "comments": "All editable sections were left as placeholders. Score set to 0."
        }, indent=2))
        return

    # --- Weak spec = capped score ---
    if is_prompt_weak(spec_text):
        print(json.dumps({
            "context": 5,
            "structure": 3,
            "scope": 5,
            "guardrails": 3,
            "style": 2,
            "safety": 2,
            "brevity": 0,
            "total": 20,
            "triggered_traps": ["Prompt spec too weak"],
            "comments": "The spec was only minimally filled. Score capped at 20."
        }, indent=2))
        return

    # Otherwise run judge
    user_prompt = rubric.format(
        context_text=context_text,
        prompt_spec=spec_text,
        task_text=task_text,
        model_output=model_output
    )

    system = (
        "You are a strict evaluator. Use the rubric JSON format only. "
        "Pay special attention to scope: penalize if the output handles out_of_scope topics, "
        "or ignores in_scope obligations. If the prompt spec is vague or generic, "
        "cap the maximum total score at 20. Be strict and never improvise."
    )

    result = chat_completion_messages(system, user_prompt, temperature=0.0)

    try:
        parsed = json.loads(result)
        print(json.dumps(parsed, indent=2))
    except Exception:
        print(json.dumps({
            "context": 0,
            "structure": 0,
            "scope": 0,
            "guardrails": 0,
            "style": 0,
            "safety": 0,
            "brevity": 0,
            "total": 0,
            "triggered_traps": ["Judge did not return valid JSON"],
            "comments": "Judge output was not valid JSON."
        }, indent=2))


if __name__ == "__main__":
    main()
