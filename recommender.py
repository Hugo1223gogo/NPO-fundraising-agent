import json
import os

import google.generativeai as genai
from dotenv import load_dotenv

from memory import get_outcome_history, get_roster
from prompts import CONTACT_EXTRACTION_PROMPT, RECOMMENDATION_PROMPT

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=api_key)


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    return text


def recommend(need: str, filters: dict | None = None) -> dict:
    model = genai.GenerativeModel("gemini-2.5-flash")

    roster = get_roster()
    outcomes = get_outcome_history()

    prompt = RECOMMENDATION_PROMPT.format(
        need=need.strip(),
        filters=json.dumps(filters or {}, indent=2),
        roster=json.dumps(roster, indent=2, default=str),
        outcomes=json.dumps(outcomes, indent=2) if outcomes else "(no prior outcomes yet)",
    )

    response = model.generate_content(prompt)
    result = json.loads(_strip_fences(response.text))

    result["need"] = need
    result["filters"] = filters or {}
    return result


def extract_contact(linkedin: str, context: str) -> dict:
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = CONTACT_EXTRACTION_PROMPT.format(
        linkedin=linkedin.strip() or "(none provided)",
        context=context.strip() or "(none provided)",
    )

    response = model.generate_content(prompt)
    result = json.loads(_strip_fences(response.text))
    result["linkedin_url"] = linkedin.strip()
    return result
