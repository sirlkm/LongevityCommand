"""Generate 2,000 synthetic cardiac patient records with realistic correlations."""

import numpy as np
import pandas as pd

SEED = 42
N = 2000


def generate() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    # --- base features ---
    age = rng.uniform(30, 60, N)
    bmi = rng.uniform(20, 38, N)
    resting_hr = rng.uniform(50, 95, N)
    hrv_rmssd = rng.uniform(20, 90, N)
    sleep_hours = rng.uniform(4, 9, N)
    stress_score = rng.integers(1, 11, N).astype(float)
    recovery_hours = rng.uniform(12, 48, N)

    # --- realistic correlations ---
    # Higher stress → lower HRV
    hrv_rmssd = np.clip(hrv_rmssd - (stress_score - 5) * 4, 20, 90)
    # Older age → slightly higher resting HR and BMI drift
    resting_hr = np.clip(resting_hr + (age - 45) * 0.3, 50, 95)
    bmi = np.clip(bmi + (age - 45) * 0.1, 20, 38)
    # Poor sleep → slower recovery
    recovery_hours = np.clip(recovery_hours - (sleep_hours - 6.5) * 3, 12, 48)

    # --- cardiac event probability (logistic model) ---
    logit = (
        -4.0
        + 0.06 * (age - 45)
        + 0.08 * (bmi - 28)
        + 0.03 * (resting_hr - 72)
        - 0.05 * (hrv_rmssd - 55)
        + 0.20 * (stress_score - 5)
        - 0.15 * (sleep_hours - 6.5)
        + 0.04 * (recovery_hours - 30)
    )
    prob = 1 / (1 + np.exp(-logit))
    cardiac_event_6mo = rng.binomial(1, prob)

    df = pd.DataFrame(
        {
            "age": np.round(age, 1),
            "bmi": np.round(bmi, 1),
            "resting_hr": np.round(resting_hr, 1),
            "hrv_rmssd": np.round(hrv_rmssd, 1),
            "sleep_hours": np.round(sleep_hours, 1),
            "stress_score": stress_score.astype(int),
            "recovery_hours": np.round(recovery_hours, 1),
            "cardiac_event_6mo": cardiac_event_6mo,
        }
    )
    return df


if __name__ == "__main__":
    df = generate()
    out = "data/synthetic_cardiac_data.csv"
    df.to_csv(out, index=False)

    print(f"Saved {len(df)} records to {out}\n")
    print("=== Data Summary ===")
    print(df.describe().round(2).to_string())
    print(f"\nEvent rate: {df['cardiac_event_6mo'].mean():.1%}")
    print(f"Events: {df['cardiac_event_6mo'].sum()} / {len(df)}")
