# Cardiac Risk Prediction Engine

Predicts 6-month cardiac event probability from biometric and lifestyle features using a Gradient Boosting classifier served via FastAPI.

## Features

| Feature | Range |
|---|---|
| age | 30–60 |
| bmi | 20–38 |
| resting_hr | 50–95 |
| hrv_rmssd | 20–90 |
| sleep_hours | 4–9 |
| stress_score | 1–10 |
| recovery_hours | 12–48 |

## Quick start

```bash
pip install -r requirements.txt
python data/generate_data.py   # create synthetic dataset
python model.py                # train model
uvicorn app:app --reload       # start API on :8000
```

## API

**POST /predict**

```json
{
  "age": 55, "bmi": 32, "resting_hr": 82,
  "hrv_rmssd": 28, "sleep_hours": 5,
  "stress_score": 8, "recovery_hours": 40
}
```

Returns `{ "risk_probability": 0.72, "risk_level": "high" }`.
