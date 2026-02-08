"""FastAPI service for cardiac risk prediction."""

from contextlib import asynccontextmanager

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field

from model import FEATURES, MODEL_PATH, SCALER_PATH


class PatientInput(BaseModel):
    age: float = Field(ge=30, le=60)
    bmi: float = Field(ge=20, le=38)
    resting_hr: float = Field(ge=50, le=95)
    hrv_rmssd: float = Field(ge=20, le=90)
    sleep_hours: float = Field(ge=4, le=9)
    stress_score: int = Field(ge=1, le=10)
    recovery_hours: float = Field(ge=12, le=48)


class PredictionOutput(BaseModel):
    risk_probability: float
    risk_level: str


_state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    _state["model"] = joblib.load(MODEL_PATH)
    _state["scaler"] = joblib.load(SCALER_PATH)
    yield
    _state.clear()


app = FastAPI(title="Cardiac Risk Prediction API", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOutput)
def predict(patient: PatientInput):
    from model import predict as _predict

    prob = _predict(patient.model_dump(), _state["model"], _state["scaler"])

    if prob < 0.15:
        level = "low"
    elif prob < 0.40:
        level = "moderate"
    else:
        level = "high"

    return PredictionOutput(risk_probability=round(prob, 4), risk_level=level)
