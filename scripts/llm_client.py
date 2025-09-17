import os, json, requests
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=ROOT / ".env")

API_KEY = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4.1")
BASE_URL = os.getenv("BASE_URL", "https://api.openai.com/v1")

HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def chat_completion(system: str, user: str, temperature: float = 0.2) -> str:
    if not API_KEY:
        raise RuntimeError("No API key found. Set API_KEY or OPENAI_API_KEY in .env")
    url = f"{BASE_URL}/chat/completions"
    payload = {
        "model": MODEL,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    }
    resp = requests.post(url, headers=HEADERS, data=json.dumps(payload), timeout=90)
    if resp.status_code != 200:
        raise RuntimeError(f"API error {resp.status_code}: {resp.text}")
    return resp.json()["choices"][0]["message"]["content"]
