import json
import os

from dotenv import load_dotenv
import google.generativeai as genai

from memory import get_all_interactions, find_interactions_by_person

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=api_key)


def answer_question(question: str) -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")

    interactions = get_all_interactions()
    context = json.dumps(interactions, indent=2)

    prompt = f"""
You are a networking memory agent.

You answer questions based only on the stored interaction history below.

Rules:
- Only use the provided interaction history
- If the answer is not in the history, say: "I could not find that in the stored interactions."
- Be concise and helpful

Stored interaction history:
{context}

User question:
{question}
"""

    response = model.generate_content(prompt)
    return response.text.strip()


def suggest_followups() -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")

    interactions = get_all_interactions()
    context = json.dumps(interactions, indent=2)

    prompt = f"""
You are an AI networking relationship manager.

Your job is to review stored networking interactions and suggest follow-up actions.

Rules:
- Look for follow_up_action fields
- Summarize the follow-ups clearly
- Group them by person if possible
- Avoid repeating identical tasks
- Be concise and practical

Stored interactions:
{context}

Return a clear list of recommended follow-up actions.
"""

    response = model.generate_content(prompt)
    return response.text.strip()


def generate_followup_email(person_name: str) -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")

    interactions = find_interactions_by_person(person_name)

    if not interactions:
        return f"I could not find any stored interactions for {person_name}."

    context = json.dumps(interactions, indent=2)

    prompt = f"""
You are helping an MBA student write a professional networking follow-up email.

Write a concise, warm, and professional follow-up email based only on the interaction history below.

Rules:
- Use the interaction history only
- Keep the tone natural and professional
- Mention 1-2 specific topics discussed
- Include a clear but not pushy next step
- Do not invent details
- End the email with exactly:

Best,
Hugo Yu

- Output only the email body

Interaction history:
{context}
"""

    response = model.generate_content(prompt)
    return response.text.strip()


def prioritize_followups() -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")

    interactions = get_all_interactions()
    context = json.dumps(interactions, indent=2)

    prompt = f"""
You are an AI networking relationship manager.

Review the stored interactions and prioritize the follow-up actions.

Prioritize based on:
- urgency implied in the follow_up_action
- career relevance
- relationship-building value
- opportunities for warm introductions

Rules:
- Use only the stored interactions
- Return the top 3 priorities
- For each priority, include:
  1. Person name
  2. Recommended action
  3. Short reason why it should be prioritized
- Be concise and practical

Stored interactions:
{context}
"""

    response = model.generate_content(prompt)
    return response.text.strip()


def relationship_insights() -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")

    interactions = get_all_interactions()
    context = json.dumps(interactions, indent=2)

    prompt = f"""
You are an AI networking strategy agent.

Review the stored networking interactions and proactively surface useful relationship insights.

Your job is to identify:
- people who seem especially valuable to follow up with
- repeated names or warm introduction opportunities
- people connected to the user's likely career goals
- gaps where a follow-up seems overdue
- patterns across conversations that could help the user network more effectively

Rules:
- Use only the stored interactions
- Be practical and specific
- Return 4 to 6 concise insights
- Each insight should be 1 to 2 sentences
- Prefer action-oriented insights over generic observations

Stored interactions:
{context}
"""

    response = model.generate_content(prompt)
    return response.text.strip()
    