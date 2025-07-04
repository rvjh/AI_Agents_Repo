from fastapi import FastAPI
from pydantic import BaseModel
from src.agent import WaterIntakeAgent
from src.water_intake_database import log_intake, get_intake_history
from src.logger import log_message, log_error

app = FastAPI()
agent = WaterIntakeAgent()

class WaterIntakeRequest(BaseModel):
    user_id: str
    intake_ml: int


@app.post("/log_intake")
async def log_water_intake(request: WaterIntakeRequest): 
    log_intake(request.user_id, request.intake_ml)
    analyze = agent.analyze_intake(request.intake_ml)
    log_message(f"User {request.user_id} logged {request.intake_ml} ml of water intake.")
    return {"message": "Water intake logged successfully", "analysis": analyze}

@app.get("/history/{user_id}")
async def get_water_intake_history(user_id: str):
    history = get_intake_history(user_id)
    return {"user_id": user_id, "history": history}