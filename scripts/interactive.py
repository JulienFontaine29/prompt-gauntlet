import argparse
from pathlib import Path
from llm_client import chat_completion

def main():
    p = argparse.ArgumentParser(description="Interactive chat with your prompt spec")
    p.add_argument("--spec", default="prompts/prompt_spec.yaml", help="Prompt spec YAML file")
    args = p.parse_args()

    system_prompt = Path(args.spec).read_text()
    print("💬 Interactive mode started. Type 'exit' or 'quit' to leave.\n")

    while True:
        user = input("You: ")
        if user.strip().lower() in ["exit", "quit"]:
            break
        try:
            reply = chat_completion(system_prompt, user, temperature=0.3)
            print(f"\n🤖 Model: {reply}\n")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
