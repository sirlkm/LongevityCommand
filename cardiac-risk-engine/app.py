"""FastAPI service for cardiac risk prediction."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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


DEMO_PATIENTS = [
    {
        "label": "Low Risk — Healthy Adult",
        "data": {
            "age": 35, "bmi": 23, "resting_hr": 58,
            "hrv_rmssd": 75, "sleep_hours": 8,
            "stress_score": 2, "recovery_hours": 16,
        },
    },
    {
        "label": "Moderate Risk — Sedentary Professional",
        "data": {
            "age": 48, "bmi": 29, "resting_hr": 76,
            "hrv_rmssd": 40, "sleep_hours": 6,
            "stress_score": 6, "recovery_hours": 32,
        },
    },
    {
        "label": "High Risk — Multiple Factors",
        "data": {
            "age": 57, "bmi": 35, "resting_hr": 90,
            "hrv_rmssd": 22, "sleep_hours": 4.5,
            "stress_score": 9, "recovery_hours": 44,
        },
    },
]

_predictor = CardiacRiskPredictor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _predictor.load()
    yield


app = FastAPI(title="Cardiac Risk Prediction API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOutput)
def predict(patient: PatientInput):
    return _predictor.predict_patient(patient.model_dump())


@app.get("/demo-patients")
def demo_patients():
    return DEMO_PATIENTS


@app.get("/")
def root():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
