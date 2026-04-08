import requests
import os
from openai import OpenAI

# =========================
# ENV VARIABLES (REQUIRED)
# =========================
API_BASE_URL = os.getenv("API_BASE_URL")  # injected by validator
API_KEY = os.getenv("API_KEY")            # injected by validator
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# Initialize OpenAI client via proxy
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

# =========================
# LLM ACTION FUNCTION
# =========================
def get_llm_action(observation):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a clinical audit expert. Analyze the case and identify mistakes in diagnosis or treatment."
            },
            {
                "role": "user",
                "content": f"Patient case: {observation}. Give a short clinical audit."
            }
        ]
    )

    return {
        "text": response.choices[0].message.content
    }

# =========================
# RUN ONE EPISODE
# =========================
def run_episode():
    print("[START] task=clinical_audit", flush=True)

    # RESET (must be POST)
    reset_res = requests.post(f"{API_BASE_URL}/reset")

    if reset_res.status_code != 200:
        print("[END] task=clinical_audit score=0 steps=0", flush=True)
        return 0

    observation = reset_res.json()

    # LLM generates action
    action = get_llm_action(observation)

    # STEP
    step_res = requests.post(f"{API_BASE_URL}/step", json=action)

    if step_res.status_code != 200:
        print("[END] task=clinical_audit score=0 steps=1", flush=True)
        return 0

    result = step_res.json()
    score = result["reward"]["score"]

    print(f"[STEP] step=1 reward={score}", flush=True)
    print(f"[END] task=clinical_audit score={score} steps=1", flush=True)

    return score

# =========================
# MAIN LOOP
# =========================
if __name__ == "__main__":
    total_score = 0
    episodes = 3

    for _ in range(episodes):
        total_score += run_episode()

    avg_score = total_score / episodes
