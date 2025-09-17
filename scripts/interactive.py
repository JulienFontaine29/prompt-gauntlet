import argparse
from pathlib import Path
from llm_client import chat_completion_messages

def main():
    p = argparse.ArgumentParser(description="Interactive chatbot with your prompt spec")
    p.add_argument("--spec", default="prompts/prompt_spec.md", help="Prompt spec Markdown file")
    args = p.parse_args()

    # Load the full spec
    spec_text = Path(args.spec).read_text()

    # Strip out Output Contract section (so JSON rules don’t dominate)
    if "## Output Contract" in spec_text:
        spec_text = spec_text.split("## Output Contract")[0]

    # Build system instructions for interactive mode
    system_prompt = (
        spec_text
        + "\n\n[INTERACTIVE MODE]\n"
        + "You are now a live interactive agent.\n"
        + "Follow your persona, style_guide, guardrails, and context strictly.\n"
        + "Respond in natural conversational language (not JSON).\n"
        + "If asked something out_of_scope, politely refuse following your guardrails.\n"
    )

    print("💬 Interactive chatbot started. Type 'exit' or 'quit' to leave.\n")

    # Initialize conversation
    history = [{"role": "system", "content": system_prompt}]

    while True:
        try:
            user_input = input("You: ")
        except KeyboardInterrupt:
            print("\n👋 Ending discussion.")
            break

        if user_input.strip().lower() in ["exit", "quit"]:
            print("👋 Ending discussion.")
            break

        history.append({"role": "user", "content": user_input})

        try:
            reply = chat_completion_messages(system_prompt, user_input, temperature=0.6)
            history.append({"role": "assistant", "content": reply})
            print(f"\n🤖 {reply}\n")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
