import argparse, json
from pathlib import Path
from llm_client import chat_completion

def main():
    p = argparse.ArgumentParser(description="Run a Prompt Gauntlet task")
    p.add_argument("task_file", help="Path to task .txt")
    p.add_argument("--spec", default="prompts/prompt_spec.yaml", help="Prompt spec YAML path")
    p.add_argument("--out", default=None, help="Output JSON/text path")
    args = p.parse_args()

    system = Path(args.spec).read_text()
    task = Path(args.task_file).read_text()
    user = f"Task:\n{task.strip()}\n\nFollow the output_contract strictly. If JSON required, return ONLY JSON."

    content = chat_completion(system, user, temperature=0.2).strip()
    try:
        parsed = json.loads(content)
        content = json.dumps(parsed, indent=2, ensure_ascii=False)
    except Exception:
        pass

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(content)
    else:
        print(content)

if __name__ == "__main__":
    main()
