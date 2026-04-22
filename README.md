# CareerOps Agent

An AI networking copilot that turns messy meeting notes into structured relationship memory. Built with Streamlit, Google Gemini, and MongoDB.

## Features
- **Analyze notes** — extract structured info from raw networking conversation notes
- **Search memory** — look up past interactions by person
- **Ask the agent** — Q&A across stored networking history, follow-up suggestions, prioritization, and email drafts

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then fill in your keys
streamlit run app.py
```

## Environment variables
See `.env.example`:
- `GEMINI_API_KEY` — Google Gemini API key
- `MONGODB_URI` — MongoDB connection string

## Deployment (Streamlit Community Cloud)
1. Push this repo to GitHub
2. Go to https://share.streamlit.io and connect the repo
3. Set the main file to `app.py`
4. Add `GEMINI_API_KEY` and `MONGODB_URI` under **Settings → Secrets**
