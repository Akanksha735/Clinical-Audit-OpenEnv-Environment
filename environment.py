import random


class Reward:
    def __init__(self, score, feedback):
        self.score = score
        self.feedback = feedback

    def to_dict(self):
        return {
            "score": self.score,
            "feedback": self.feedback
        }


class ClinicalAuditEnv:
    def __init__(self):
        self.done = False
        self.current_case = None
        self.current_task = None

        # Sample cases
        self.cases = [
            {
                "patient": {
                    "symptoms": ["fever", "cough"],
                    "history": ["no chronic disease"]
                },
                "ground_truth": "viral infection - no antibiotics",
                "task_type": "easy"
            },
            {
                "patient": {
                    "symptoms": ["chest pain"],
                    "history": ["diabetes"]
                },
                "ground_truth": "possible cardiac issue - ECG required",
                "task_type": "hard"
            },
            {
                "patient": {
                    "symptoms": ["fatigue", "weight loss"],
                    "history": ["smoker"]
                },
                "ground_truth": "possible cancer - further tests needed",
                "task_type": "medium"
            }
        ]

    def reset(self):
        """Reset environment safely"""
        self.done = False

        self.current_case = random.choice(self.cases)
        self.current_task = self.current_case["task_type"]

        
        return {
            "patient": self.current_case["patient"],
            "task_type": self.current_task
        }

    def step(self, action):
        """Take action safely"""

        if self.done:
            return None, Reward(0, "Episode already finished").to_dict(), True, {}

        
        if isinstance(action, dict):
            response_text = action.get("response", "")
        else:
            response_text = str(action)

        ground_truth = self.current_case["ground_truth"]

       
        score = 0

        if "antibiotics" in response_text.lower() and "no antibiotics" in ground_truth:
            score = 0  # wrong
        elif "ecg" in response_text.lower() and "ecg" in ground_truth.lower():
            score = 1
        elif "tests" in response_text.lower():
            score = 0.5
        else:
            score = 0.2

        self.done = True

        reward = Reward(
            score=score,
            feedback=f"Task: {self.current_task}, Score: {score}"
        )

        
        return None, reward.to_dict(), True, {}