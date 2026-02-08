"""Cardiac risk prediction model — train, evaluate, and persist."""

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

FEATURES = [
    "age",
    "bmi",
    "resting_hr",
    "hrv_rmssd",
    "sleep_hours",
    "stress_score",
    "recovery_hours",
]
TARGET = "cardiac_event_6mo"
MODEL_PATH = "model.joblib"
SCALER_PATH = "scaler.joblib"


def load_data(path: str = "data/synthetic_cardiac_data.csv") -> pd.DataFrame:
    return pd.read_csv(path)


def train(df: pd.DataFrame) -> dict:
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    clf = GradientBoostingClassifier(
        n_estimators=200, max_depth=4, learning_rate=0.1, random_state=42
    )
    clf.fit(X_train_s, y_train)

    y_prob = clf.predict_proba(X_test_s)[:, 1]
    y_pred = clf.predict(X_test_s)
    auc = roc_auc_score(y_test, y_prob)
    report = classification_report(y_test, y_pred)

    joblib.dump(clf, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    return {"auc": auc, "report": report, "model": clf, "scaler": scaler}


def predict(patient: dict, model=None, scaler=None) -> float:
    if model is None:
        model = joblib.load(MODEL_PATH)
    if scaler is None:
        scaler = joblib.load(SCALER_PATH)

    row = pd.DataFrame([patient])[FEATURES]
    row_s = scaler.transform(row)
    return float(model.predict_proba(row_s)[:, 1][0])


if __name__ == "__main__":
    df = load_data()
    result = train(df)
    print(f"ROC-AUC: {result['auc']:.4f}")
    print(result["report"])
