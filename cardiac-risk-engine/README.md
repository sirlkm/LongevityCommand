# Cardiac Risk Prediction Engine

Predicts 6-month cardiac event probability from biometric and lifestyle features using an XGBoost classifier served via FastAPI.

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

## Quick start (local)

```bash
pip install -r requirements.txt
python data/generate_data.py   # create synthetic dataset
python model.py                # train model
uvicorn app:app --reload       # start API on :8000
```

## Deploy to Render.com (free tier)

### Option A: Blueprint (recommended)

1. Push this repo to GitHub
2. Go to https://dashboard.render.com
3. **New > Blueprint** → connect your GitHub repo
4. Render auto-detects `render.yaml` and deploys
5. Wait ~5 min for build → your URL: `https://cardiac-risk-engine.onrender.com`

### Option B: Manual Web Service

1. Push this repo to GitHub
2. Go to https://dashboard.render.com → **New > Web Service**
3. Connect your GitHub repo
4. Settings:
   - **Name:** `cardiac-risk-engine`
   - **Runtime:** Docker
   - **Dockerfile Path:** `./cardiac-risk-engine/Dockerfile`
   - **Docker Context:** `./cardiac-risk-engine`
   - **Plan:** Free
5. Click **Create Web Service**
6. Wait for build → get your public URL

### Free tier notes

- Spins down after 15 min of inactivity (first request after sleep takes ~30s)
- 512 MB RAM, 0.1 CPU — sufficient for this model
- HTTPS included automatically

## Alternative: Railway.app

```bash
npm install -g @railway/cli
cd cardiac-risk-engine
railway login
railway init
railway up
```

Railway auto-detects the Dockerfile. Free trial gives $5 credit.

## Alternative: ngrok (instant, temporary)

```bash
cd cardiac-risk-engine
uvicorn app:app --port 8000 &
ngrok http 8000
```

Gives you a public URL immediately. Good for demos and screen recordings.

## API

**POST /predict**

```json
{
  "age": 55, "bmi": 32, "resting_hr": 82,
  "hrv_rmssd": 28, "sleep_hours": 5,
  "stress_score": 8, "recovery_hours": 40
}
```

Returns:
```json
{
  "risk_score": 72,
  "risk_level": "HIGH",
  "timeline": [0.78, 0.84, 0.89, 0.95, 0.99, 0.99],
  "top_risk_factors": ["Low HRV (poor autonomic function)", "..."],
  "recommendation": "Urgent cardiac workup recommended. ..."
}
```

**GET /demo-patients** — returns 3 example patients (low/moderate/high risk)

**GET /health** — returns `{"status": "ok"}`

**GET /** — serves the web UI
