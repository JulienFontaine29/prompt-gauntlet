# Prompt Gauntlet 🏟️

Welcome to **Prompt Gauntlet** — a hands-on 1-hour workshop where you’ll build, test, and battle your own AI agent prompt.

---

## ⚡ Setup

### 1. Clone the repo

```bash
# macOS / Linux
git clone https://github.com/YOURNAME/prompt-gauntlet.git
cd prompt-gauntlet

# Windows (PowerShell)
git clone https://github.com/YOURNAME/prompt-gauntlet.git
cd prompt-gauntlet


### 2. Create a Virtual Envrionment

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

### 3. Install dependencies

#Both macOS / Linux / Windows
pip install -r requirements.txt

### 4. Configure API key

# Both macOS / Linux / Windows
cp .env.example .env

API_KEY=sk-xxxx
MODEL=gpt-4.1
BASE_URL=https://api.openai.com/v1


### How to Play

1. Pick a Track:


- Choose one of the tasks in tasks/:
- tasks/clinical/task.txt → explain lab results
- tasks/customer_service/task.txt → handle refund request
- tasks/coaching/task.txt → GLP-1 coaching plan
- Each has a matching context in contexts/.

2. Build Your Agent:

- Edit prompts/prompt_spec.md and fill in:

    - Objective
    - Audience
    - Persona
    - Scope (in-scope + out-of-scope)
    - Style guide
    - Context (copy facts from contexts/)
    - Guardrails
    - Output Contract (JSON schema + refusal JSON fallback)

3. Run Task Mode

# macOS / Linux
python3 scripts/run_task.py tasks/clinical/task.txt --out submissions/team1.json

# Windows (PowerShell)
python scripts/run_task.py tasks/clinical/task.txt --out submissions/team1.json


4. Run Interactive Mode

# macOS / Linux
python3 scripts/interactive.py --spec prompts/prompt_spec.md

# Windows (PowerShell)
python scripts/interactive.py --spec prompts/prompt_spec.md

5. Judge Your Submission

# macOS / Linux
python3 scripts/judge.py submissions/team1.json \
  --task tasks/clinical/task.txt \
  --context contexts/clinical_context.md

# Windows (PowerShell, all on one line)
python scripts/judge.py submissions/team1.json --task tasks/clinical/task.txt --context contexts/clinical_context.md


6. Switch Models 


Change .env file

MODEL=gpt-5

### Folder Guide

- prompts/ → Your spec (prompt_spec.md), example (prompt_spec_template.md), rubric (judge_prompt.txt).
- tasks/ → Challenge definitions (clinical, customer service, coaching).
- contexts/ → Ground truth each agent must follow.
- scripts/ → Tools:
    - run_task.py (Task Mode JSON)
    - interactive.py (Chatbot mode)
    - judge.py (Scoring)
    - llm_client.py (API client)
- submissions/ → Where your outputs get saved.
- .env.example → Template for environment variables.
- requirements.txt → Python dependencies.