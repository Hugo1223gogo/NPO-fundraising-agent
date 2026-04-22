import json
import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=api_key)


def extract_networking_info(note: str) -> dict:
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
Extract structured networking information from the meeting note below.

Return valid JSON only with exactly these keys:
- person_name
- company
- topics_discussed
- suggested_connections
- follow_up_action

Rules:
- topics_discussed should be a list of strings
- suggested_connections should be a list of strings
- If information is missing, use an empty string or empty list
- Do not include markdown or code fences

Meeting note:
{note}
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)