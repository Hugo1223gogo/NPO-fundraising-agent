# U4H Donor Recommendation Agent

A prototype AI fundraising copilot for U4H. Given a fundraising need, it recommends **who to contact**, **through which pathway**, **why**, and **what to do next** — grounded in a roster of supporters active at peer nonprofits (Mothers2Mothers, HelpMum, Assist International) and a feedback loop that captures outreach outcomes.

## Features
- **Get Recommendations** — describe a fundraising need; the agent returns up to 3 candidates, each with a 0–100 helpfulness score, pathway (direct / warm intro / event connection), rationale, tactical approach tips, and a concrete next step.
- **Browse Roster** — search the seeded roster of demo supporters.
- **Feedback & History** — record the outcome of each outreach (success / no_response / declined). Outcomes are fed back into the next recommendation so the agent improves over time.

## Stack
Streamlit · Google Gemini (`gemini-2.5-flash`) · MongoDB · pandas.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then fill in your keys
streamlit run app.py
```

The roster auto-seeds from [data/demo_roster.csv](data/demo_roster.csv) on first run. Edit the CSV and call `reseed_roster(load_roster_from_csv())` from a Python shell (or wipe the `roster` collection) to refresh.

## Environment variables
See `.env.example`:
- `GEMINI_API_KEY` — Google Gemini API key
- `MONGODB_URI` — MongoDB connection string

Database: `u4h_fundraising` · collections: `roster`, `recommendations`, `feedback`.

## Deployment (Streamlit Community Cloud)
1. Push this repo to GitHub
2. Connect at https://share.streamlit.io
3. Main file: `app.py`
4. Add `GEMINI_API_KEY` and `MONGODB_URI` under **Settings → Secrets**
