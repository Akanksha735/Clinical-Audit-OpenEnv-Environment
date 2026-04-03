from pydantic import BaseModel
from typing import List, Optional

class Patient(BaseModel):
    symptoms: List[str]
    history: List[str]

class Decision(BaseModel):
    text: str

class Observation(BaseModel):
    patient: Patient
    decision: Decision
    task_type: str  # "easy", "medium", "hard"

class Action(BaseModel):
    response: str

class Reward(BaseModel):
    score: float
    feedback: Optional[str] = None