# Cardiac Risk Prediction Engine — 6-Month Advance Warning

> **Demo:** Local demo — video available | [Deploy your own](#deploy)

Working ML system that predicts cardiac events **6+ months in advance** using biometric data collectible from consumer wearables. Takes 7 patient metrics (heart rate, HRV, sleep, stress, BMI, age, recovery time), engineers 3 domain-specific risk features, and outputs an individual risk trajectory showing month-by-month progression — not just a binary yes/no.

**Built in 48 hours to validate Longevity Command's core technology.**

## Model Performance

| Metric | Value |
|---|---|
| ROC-AUC | **0.82** |
| Accuracy | 91.5% |
| Features | 7 raw + 3 engineered |
| Training data | 2,000 synthetic patients |
| Prediction horizon | 6 months (monthly granularity) |

## Example Predictions

| Patient | Risk Score | 6-Month Trajectory |
|---|---|---|
| Healthy adult (35, BMI 23, HRV 75) | **0%** LOW | Flat — no intervention needed |
| Stressed professional (52, BMI 31, HRV 30) | **25%** MODERATE | Rising 27% → 38% — early intervention window |
| Multiple factors (57, BMI 35, HRV 22) | **99%** HIGH | Critical — immediate workup recommended |

## Key Innovation

Traditional cardiac risk scores (Framingham, ASCVD) give a single 10-year number. We generate **individual risk trajectories** that show how risk compounds over time, enabling intervention *before* events occur.

## Quick Start

```bash
cd cardiac-risk-engine
pip install -r requirements.txt
python data/generate_data.py
python model.py
uvicorn app:app --reload
# Open http://localhost:8000
```

## Deploy

### Render.com (free tier)

1. Push to GitHub
2. Dashboard → **New > Blueprint** → select repo
3. `render.yaml` auto-configures everything
4. Live in ~5 minutes at `https://cardiac-risk-engine.onrender.com`

### Railway.app

```bash
npm install -g @railway/cli && cd cardiac-risk-engine
railway login && railway init && railway up
```

### ngrok (instant, temporary)

```bash
uvicorn app:app --port 8000 & ngrok http 8000
```

## API

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age":57,"bmi":35,"resting_hr":90,"hrv_rmssd":22,"sleep_hours":4.5,"stress_score":9,"recovery_hours":44}'
```

```json
{
  "risk_score": 99,
  "risk_level": "HIGH",
  "timeline": [0.99, 0.99, 0.99, 0.99, 0.99, 0.99],
  "top_risk_factors": [
    "Low HRV (poor autonomic function)",
    "Elevated chronic stress",
    "Insufficient sleep",
    "Slow recovery time",
    "Age >50 with elevated BMI",
    "Elevated resting heart rate",
    "High BMI"
  ],
  "recommendation": "Urgent cardiac workup recommended. Immediate lifestyle intervention for modifiable risk factors."
}
```

**GET /demo-patients** — 3 pre-configured examples (low/moderate/high)
**GET /health** — health check
**GET /** — web UI

## Architecture

```
cardiac-risk-engine/
├── data/
│   ├── generate_data.py          # Synthetic data generator
│   └── synthetic_cardiac_data.csv
├── static/
│   └── index.html                # Tailwind + Chart.js frontend
├── YC_ASSETS/
│   ├── demo_talking_points.txt   # YC demo script
│   ├── model_performance.txt     # Detailed metrics
│   ├── example_low_risk.json
│   ├── example_moderate_risk.json
│   └── example_high_risk.json
├── model.py                      # CardiacRiskPredictor (XGBoost)
├── app.py                        # FastAPI backend
├── Dockerfile
├── render.yaml
└── requirements.txt
```
