import argparse, json
from pathlib import Path
from llm_client import chat_completion_messages

def main():
    p = argparse.ArgumentParser(description="Judge a team submission")
    p.add_argument("candidate_json", help="Path to team’s model output JSON")
    p.add_argument("--task", required=True, help="Task file path")
    p.add_argument("--spec", default="prompts/prompt_spec.md", help="Team’s prompt spec file")
    p.add_argument("--context", required=True, help="Context file path")
    args = p.parse_args()

    # Load inputs
    rubric = Path("prompts/judge_prompt.txt").read_text()
    spec_text = Path(args.spec).read_text()
    task_text = Path(args.task).read_text()
    context_text = Path(args.context).read_text()
    model_output = Path(args.candidate_json).read_text()

    # Format the judge prompt
    user_prompt = rubric.format(
        context_text=context_text,
        prompt_spec=spec_text,
        task_text=task_text,
        model_output=model_output
    )

    system = "You are a strict evaluator. Use the rubric JSON format only. Pay special attention to scope: penalize if the output handles out_of_scope topics, or ignores in_scope obligations. Pay sepcial care to anything that is out of scope."
    result = chat_completion_messages(system, user_prompt, temperature=0.0)

    try:
        parsed = json.loads(result)
        print(json.dumps(parsed, indent=2))
    except Exception:
        print(result)

if __name__ == "__main__":
    main()
