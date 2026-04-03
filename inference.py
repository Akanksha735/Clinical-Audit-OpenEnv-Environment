import os
import time
import requests


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "baseline-agent")
HF_TOKEN = os.getenv("HF_TOKEN", None)


def safe_json(response):
    try:
        return response.json()
    except Exception:
        return None


def run_episode():
    try:
        # Reset environment
        reset_res = requests.get(f"{API_BASE_URL}/reset", timeout=5)
        
        if reset_res.status_code != 200:
            print("❌ Reset failed:", reset_res.text)
            return 0
        
        observation = safe_json(reset_res)
        
        if observation is None:
            print("❌ Invalid JSON from /reset")
            return 0

        print("\n--- NEW CASE ---")
        print(observation)

        # Simple baseline agent (static reasoning)
        action = {
            "response": "Patient requires further diagnostic evaluation before treatment decisions"
        }

        # Take step
        step_res = requests.post(
            f"{API_BASE_URL}/step",
            json=action,
            timeout=5
        )

        if step_res.status_code != 200:
            print("❌ Step failed:", step_res.text)
            return 0

        result = safe_json(step_res)

        if result is None:
            print("❌ Invalid JSON from /step")
            return 0

        print("\n--- RESULT ---")
        print(result)

        score = result.get("reward", {}).get("score", 0)
        return score

    except requests.exceptions.RequestException as e:
        print("❌ Network error:", str(e))
        return 0

    except Exception as e:
        print("❌ Unexpected error:", str(e))
        return 0


# =========================
# MAIN LOOP
# =========================
if __name__ == "__main__":
    print("⏳ Waiting for server...")

   
    time.sleep(2)

    episodes = 3
    total_score = 0

    for i in range(episodes):
        print(f"\n=== Episode {i+1} ===")
        score = run_episode()
        total_score += score

    avg_score = total_score / episodes if episodes > 0 else 0
    print(f"\n🔥 Final Average Score: {avg_score}")
