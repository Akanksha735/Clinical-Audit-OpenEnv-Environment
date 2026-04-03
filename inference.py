import requests
import time

BASE_URL = "http://127.0.0.1:8000"


def safe_json(response):
    """Safely parse JSON response"""
    try:
        return response.json()
    except Exception:
        print("❌ Failed to parse JSON")
        print("Raw response:", response.text)
        return None


def run_episode():
    # ---- RESET ----
    try:
        reset_res = requests.get(f"{BASE_URL}/reset")
    except Exception as e:
        print("❌ Server not running:", e)
        return 0

    if reset_res.status_code != 200:
        print("❌ Reset failed:", reset_res.text)
        return 0

    observation = safe_json(reset_res)
    if observation is None:
        return 0

    print("\n--- NEW CASE ---")
    print(observation)

    # ---- ACTION ----
    action = {
        "response": "Doctor prescribed unnecessary antibiotics, missed lab tests, failed to confirm diagnosis, and ignored symptoms"
    }

    # ---- STEP ----
    try:
        step_res = requests.post(f"{BASE_URL}/step", json=action)
    except Exception as e:
        print("❌ Step request failed:", e)
        return 0

    if step_res.status_code != 200:
        print("❌ Step failed:", step_res.text)
        return 0

    result = safe_json(step_res)
    if result is None:
        return 0

    print("\n--- RESULT ---")
    print(result)

    # ---- HANDLE DONE STATE ----
    if result.get("done") is True:
        print("✅ Episode completed")

    # ---- SAFE SCORE EXTRACTION ----
    reward = result.get("reward", {})
    score = reward.get("score", 0)

    return score


if __name__ == "__main__":
    total_score = 0
    episodes = 3

    # Give server time to start (IMPORTANT FIX)
    print("⏳ Waiting for server...")
    time.sleep(2)

    for i in range(episodes):
        print(f"\n=== Episode {i+1} ===")
        score = run_episode()
        total_score += score

        # Avoid "episode finished" error
        time.sleep(1)

    avg_score = total_score / episodes
    print(f"\n🔥 Final Average Score: {avg_score}")