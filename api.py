from fastapi import FastAPI
from pydantic import BaseModel
from environment import ClinicalAuditEnv

app = FastAPI()
env = ClinicalAuditEnv()


class ActionInput(BaseModel):
    response: str


@app.get("/reset")
def reset():
    return env.reset()


@app.post("/step")
def step(action: ActionInput):
    obs, reward, done, info = env.step(action.dict())

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }