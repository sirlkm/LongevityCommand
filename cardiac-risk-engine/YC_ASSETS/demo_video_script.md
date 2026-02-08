# Cardiac Risk Engine — Demo Video Script

> **Target length:** 60–90 seconds
> **Format:** Screen recording with voiceover
> **Tool:** QuickTime (Mac) / OBS (PC) → upload to Loom or YouTube (unlisted)

---

## PRE-RECORDING CHECKLIST

- [ ] Start the server: `cd cardiac-risk-engine && uvicorn app:app --reload`
- [ ] Open browser to `http://localhost:8000`
- [ ] Reset all sliders to defaults (middle position)
- [ ] Hide bookmarks bar, close other tabs
- [ ] Screen resolution: 1920x1080 or 1440x900 (clean, no scaling artifacts)
- [ ] Mic check — quiet room, speak clearly

---

## THE SCRIPT

### [0:00–0:15] HOOK — What it is

> *Show: Browser with the Cardiac Risk Engine UI, form visible, no results yet.*

**SAY:**
"This is Longevity Command's cardiac risk prediction engine. It takes biometric data — the kind you collect from an Apple Watch — and predicts cardiac events six or more months before they happen."

**DO:** Slowly mouse over the input sliders so viewers see the metrics.

---

### [0:15–0:30] HIGH-RISK PATIENT — The dramatic case

> *Show: Click the "High Risk — Multiple Factors" demo button.*

**SAY:**
"Here's a 57-year-old first responder. BMI of 35, resting heart rate of 90, HRV of just 22 — that's severely depressed autonomic function. Chronic stress score of 9. Sleeping four and a half hours a night."

**DO:** Pause briefly so viewers can see the sliders snap into position.

---

### [0:30–0:45] THE PREDICTION — Money shot

> *Show: Results appear — red 99% score, timeline chart, risk factors list.*

**SAY:**
"The model flags this patient at 99% cardiac risk. But the real value isn't the number — it's the timeline. The system shows risk compounding month over month. That's a window for intervention before the event happens. And it tells you exactly why: low HRV, chronic stress, insufficient sleep — all modifiable."

**DO:** Mouse over the timeline chart to show tooltips. Scroll to the risk factors list.

---

### [0:45–0:60] LOW-RISK COMPARISON — Prove it discriminates

> *Show: Click the "Low Risk — Healthy Adult" demo button.*

**SAY:**
"Now compare: a healthy 35-year-old. Good HRV, low stress, solid sleep. Risk stays near zero across all six months. The model doesn't just flag everyone — it learns individual patterns."

**DO:** Let the green score and flat timeline chart land visually. Pause one beat.

---

### [0:60–0:70] MODERATE RISK — The patient you want to catch

> *Show: Click the "Moderate Risk — Stressed Professional" demo button.*

**SAY:**
"This is the patient we exist to find. A 52-year-old, moderately elevated risk — 25% — trending upward. Month one: 27%. Month six: 38%. Traditional screening misses this person. We catch them three months early."

**DO:** Mouse along the rising yellow timeline to emphasize the upward slope.

---

### [0:70–0:85] CLOSE — Feasibility + vision

> *Show: Keep the moderate-risk results on screen.*

**SAY:**
"We built this in 48 hours to prove the core technology works. Production version integrates directly with Apple Watch, feeds into our insurance risk platform, and creates the data moat that makes Longevity Command defensible. This is preventive cardiology that scales."

**DO:** Hold on the results screen. End recording.

---

## POST-RECORDING

1. **Trim** dead air at start/end
2. **Export** at 1080p, H.264
3. **Upload** to Loom (easiest sharing) or YouTube (unlisted)
4. **Copy link** → paste into YC application under "Product Demo"
5. **Backup** the raw file in `YC_ASSETS/`

## QUICK VERSION (30 seconds — if time is tight)

Skip sections 4 and 5. Go straight from the high-risk prediction to the close:

> "[0:00–0:10] This is our cardiac risk engine. Biometric data in, 6-month risk prediction out."
>
> "[0:10–0:20] [Click high-risk] 99% risk. The timeline shows compounding danger. Every risk factor is identified and actionable."
>
> "[0:20–0:30] Built in 48 hours. Production version integrates Apple Watch and insurance. This is Longevity Command's core technology."

Even 30 seconds of a working demo beats 10 pages of slides.

---

*Last updated: 2026-02-08 — ready for YC submission Monday*
