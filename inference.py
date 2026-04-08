import requests
import os
from openai import OpenAI

# =========================
# URLs (IMPORTANT)
# =========================
OPENENV_URL = "https://akanksha11aaron-clinical-audit-env.hf.space"

LLM_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# LLM Client (proxy)
client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=API_KEY
)

def get_llm_action(observation):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a clinical audit expert."},
            {"role": "user", "content": f"Analyze this case: {observation}"}
        ]
    )

    return {
        "text": response.choices[0].message.content
    }

def run_episode():
    print("[START] task=clinical_audit", flush=True)

    # RESET
    reset_res = requests.post(f"{OPENENV_URL}/reset")

    if reset_res.status_code != 200:
        print("[END] task=clinical_audit score=0 steps=0", flush=True)
        return 0

    observation = reset_res.json()

    # LLM ACTION
    action = get_llm_action(observation)

    # STEP
    step_res = requests.post(f"{OPENENV_URL}/step", json=action)

    if step_res.status_code != 200:
        print("[END] task=clinical_audit score=0 steps=1", flush=True)
        return 0

    result = step_res.json()
    score = result["reward"]["score"]

    print(f"[STEP] step=1 reward={score}", flush=True)
    print(f"[END] task=clinical_audit score={score} steps=1", flush=True)

    return score


if __name__ == "__main__":
    total = 0
    episodes = 3

    for _ in range(episodes):
        total += run_episode()

    avg = total / episodes
