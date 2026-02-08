"""Cardiac risk prediction model — train, evaluate, predict."""

import json
import pickle

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

RAW_FEATURES = [
    "age", "bmi", "resting_hr", "hrv_rmssd",
    "sleep_hours", "stress_score", "recovery_hours",
]
ENGINEERED_FEATURES = ["cardiovascular_stress", "recovery_risk", "metabolic_load"]
ALL_FEATURES = RAW_FEATURES + ENGINEERED_FEATURES
TARGET = "cardiac_event_6mo"
MODEL_PATH = "cardiac_model.pkl"


class CardiacRiskPredictor:
    def __init__(self):
        self.model: XGBClassifier | None = None
        self.scaler: StandardScaler | None = None

    # ── feature engineering ──────────────────────────────────────────
    @staticmethod
    def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["cardiovascular_stress"] = (
            df["resting_hr"] * df["stress_score"]
        ) / df["hrv_rmssd"]
        df["recovery_risk"] = df["recovery_hours"] / df["sleep_hours"]
        df["metabolic_load"] = df["bmi"] * (11 - df["stress_score"]) / 10
        return df

    # ── training ─────────────────────────────────────────────────────
    def train(self, csv_path: str = "data/synthetic_cardiac_data.csv") -> dict:
        df = pd.read_csv(csv_path)
        df = self.engineer_features(df)

        X = df[ALL_FEATURES]
        y = df[TARGET]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y,
        )

        self.scaler = StandardScaler()
        X_train_s = self.scaler.fit_transform(X_train)
        X_test_s = self.scaler.transform(X_test)

        self.model = XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.08,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=(y_train == 0).sum() / max((y_train == 1).sum(), 1),
            eval_metric="logloss",
            random_state=42,
        )
        self.model.fit(X_train_s, y_train)

        y_prob = self.model.predict_proba(X_test_s)[:, 1]
        y_pred = self.model.predict(X_test_s)

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, y_prob),
        }

        self.save()
        return metrics

    # ── persistence ──────────────────────────────────────────────────
    def save(self, path: str = MODEL_PATH):
        with open(path, "wb") as f:
            pickle.dump({"model": self.model, "scaler": self.scaler}, f)

    def load(self, path: str = MODEL_PATH):
        with open(path, "rb") as f:
            data = pickle.load(f)
        self.model = data["model"]
        self.scaler = data["scaler"]

    # ── core prediction ──────────────────────────────────────────────
    def _base_risk(self, patient: dict) -> float:
        row = pd.DataFrame([patient])
        row = self.engineer_features(row)
        X = row[ALL_FEATURES]
        X_s = self.scaler.transform(X)
        return float(self.model.predict_proba(X_s)[:, 1][0])

    # ── timeline: months 1-6 ─────────────────────────────────────────
    def predict_risk_timeline(self, patient: dict) -> list[float]:
        base = self._base_risk(patient)
        timeline = []
        for month in range(1, 7):
            score = base * (1 + month * 0.08)
            timeline.append(min(score, 0.99))
        return timeline

    # ── full patient prediction ──────────────────────────────────────
    def predict_patient(self, patient: dict) -> dict:
        base = self._base_risk(patient)
        risk_pct = int(round(base * 100))
        risk_pct = max(0, min(risk_pct, 100))

        if risk_pct < 20:
            level = "LOW"
        elif risk_pct < 50:
            level = "MODERATE"
        else:
            level = "HIGH"

        timeline = self.predict_risk_timeline(patient)

        # identify top risk factors
        top_factors = []
        if patient.get("hrv_rmssd", 999) < 35:
            top_factors.append("Low HRV (poor autonomic function)")
        if patient.get("stress_score", 0) >= 7:
            top_factors.append("Elevated chronic stress")
        if patient.get("sleep_hours", 99) < 5.5:
            top_factors.append("Insufficient sleep")
        if patient.get("recovery_hours", 0) > 36:
            top_factors.append("Slow recovery time")
        if patient.get("age", 0) > 50 and patient.get("bmi", 0) > 30:
            top_factors.append("Age >50 with elevated BMI")
        if patient.get("resting_hr", 0) > 85:
            top_factors.append("Elevated resting heart rate")
        if patient.get("bmi", 0) > 32:
            top_factors.append("High BMI")
        if not top_factors:
            top_factors.append("No major individual risk factors identified")

        # recommendation
        if level == "LOW":
            rec = "Continue current lifestyle. Annual cardiac screening recommended."
        elif level == "MODERATE":
            rec = ("Schedule cardiac evaluation within 3 months. "
                   "Focus on stress management and sleep optimization.")
        else:
            rec = ("Urgent cardiac workup recommended. "
                   "Immediate lifestyle intervention for modifiable risk factors.")

        return {
            "risk_score": risk_pct,
            "risk_level": level,
            "timeline": [round(t, 4) for t in timeline],
            "top_risk_factors": top_factors,
            "recommendation": rec,
        }


# ── main: train + demo ──────────────────────────────────────────────
if __name__ == "__main__":
    predictor = CardiacRiskPredictor()

    print("=" * 60)
    print("TRAINING CARDIAC RISK MODEL")
    print("=" * 60)
    metrics = predictor.train()
    for k, v in metrics.items():
        print(f"  {k:>12s}: {v:.4f}")
    print(f"\nModel saved to {MODEL_PATH}")

    # ── 3 example patients ───────────────────────────────────────
    examples = [
        {
            "label": "LOW RISK",
            "data": {
                "age": 35, "bmi": 23, "resting_hr": 58,
                "hrv_rmssd": 75, "sleep_hours": 8,
                "stress_score": 2, "recovery_hours": 16,
            },
        },
        {
            "label": "MODERATE RISK",
            "data": {
                "age": 48, "bmi": 29, "resting_hr": 76,
                "hrv_rmssd": 40, "sleep_hours": 6,
                "stress_score": 6, "recovery_hours": 32,
            },
        },
        {
            "label": "HIGH RISK",
            "data": {
                "age": 57, "bmi": 35, "resting_hr": 90,
                "hrv_rmssd": 22, "sleep_hours": 4.5,
                "stress_score": 9, "recovery_hours": 44,
            },
        },
    ]

    for ex in examples:
        result = predictor.predict_patient(ex["data"])
        print(f"\n{'=' * 60}")
        print(f"PATIENT: {ex['label']}")
        print(f"{'=' * 60}")
        print(f"  Input:        {ex['data']}")
        print(f"  Risk Score:   {result['risk_score']}%")
        print(f"  Risk Level:   {result['risk_level']}")
        print(f"  Timeline:     {['%.1f%%' % (t*100) for t in result['timeline']]}")
        print(f"  Top Factors:  {result['top_risk_factors']}")
        print(f"  Rec:          {result['recommendation']}")
