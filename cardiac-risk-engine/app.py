"""FastAPI service for cardiac risk prediction."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field

from model import CardiacRiskPredictor


class PatientInput(BaseModel):
    age: float = Field(ge=30, le=60)
    bmi: float = Field(ge=20, le=38)
    resting_hr: float = Field(ge=50, le=95)
    hrv_rmssd: float = Field(ge=20, le=90)
    sleep_hours: float = Field(ge=4, le=9)
    stress_score: int = Field(ge=1, le=10)
    recovery_hours: float = Field(ge=12, le=48)


class PredictionOutput(BaseModel):
    risk_score: int
    risk_level: str
    timeline: list[float]
    top_risk_factors: list[str]
    recommendation: str


_predictor = CardiacRiskPredictor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _predictor.load()
    yield


app = FastAPI(title="Cardiac Risk Prediction API", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOutput)
def predict(patient: PatientInput):
    return _predictor.predict_patient(patient.model_dump())
