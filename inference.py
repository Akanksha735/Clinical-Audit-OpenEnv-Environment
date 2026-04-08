import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def run_episode():
    try:
        # RESET
        reset_res = requests.post(f"{API_BASE_URL}/reset")
        obs = reset_res.json()

        # Print START
        print("[START] task=clinical_audit", flush=True)

        # ACTION
        action = {
            "response": "Doctor prescribed unnecessary antibiotics and missed proper diagnosis"
        }

        # STEP
        step_res = requests.post(f"{API_BASE_URL}/step", json=action)
        result = step_res.json()

        reward = result["reward"]["score"]

        # Print STEP
        print(f"[STEP] step=1 reward={reward}", flush=True)

        # Print END
        print(f"[END] task=clinical_audit score={reward} steps=1", flush=True)

        return reward

    except Exception as e:
        print(f"Error: {e}", flush=True)
        return 0


if __name__ == "__main__":
    run_episode()
