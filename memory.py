import os
from datetime import datetime, timezone

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI not found in .env")

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
db = client["u4h_fundraising"]

roster_col = db["roster"]
recommendations_col = db["recommendations"]
feedback_col = db["feedback"]


def test_connection() -> str:
    client.admin.command("ping")
    return "MongoDB connection successful"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def seed_roster_if_empty(people: list[dict]) -> int:
    if roster_col.count_documents({}) > 0:
        return 0
    if not people:
        return 0
    roster_col.insert_many(people)
    return len(people)


def reseed_roster(people: list[dict]) -> int:
    roster_col.delete_many({})
    if not people:
        return 0
    roster_col.insert_many(people)
    return len(people)


def get_roster() -> list[dict]:
    return list(roster_col.find({}, {"_id": 0}))


def add_person_to_roster(person: dict) -> str:
    doc = {**person, "added_at": _now_iso()}
    result = roster_col.insert_one(doc)
    return str(result.inserted_id)


def find_person_by_name(name: str) -> dict | None:
    return roster_col.find_one(
        {"name": {"$regex": f"^{name}$", "$options": "i"}},
        {"_id": 0},
    )


def save_recommendation(rec: dict) -> str:
    doc = {**rec, "created_at": _now_iso()}
    result = recommendations_col.insert_one(doc)
    return str(result.inserted_id)


def get_recommendations(limit: int = 50) -> list[dict]:
    return list(recommendations_col.find().sort("_id", -1).limit(limit))


def get_recommendation_by_id(rec_id: str):
    try:
        return recommendations_col.find_one({"_id": ObjectId(rec_id)})
    except Exception:
        return None


def save_feedback(rec_id: str, person_name: str, outcome: str, note: str = "") -> str:
    entry = {
        "recommendation_id": rec_id,
        "person_name": person_name,
        "outcome": outcome,
        "note": note,
        "created_at": _now_iso(),
    }
    result = feedback_col.insert_one(entry)
    return str(result.inserted_id)


def get_feedback(limit: int = 50) -> list[dict]:
    return list(feedback_col.find({}, {"_id": 0}).sort("_id", -1).limit(limit))


def get_feedback_for_person(name: str) -> list[dict]:
    target = (name or "").strip()
    if not target:
        return []
    return list(
        feedback_col.find(
            {"person_name": {"$regex": f"^{target}$", "$options": "i"}},
            {"_id": 0},
        ).sort("_id", -1)
    )


def get_outcome_history(limit: int = 100) -> list[dict]:
    return [
        {
            "person_name": fb.get("person_name"),
            "outcome": fb.get("outcome"),
            "note": fb.get("note", ""),
        }
        for fb in feedback_col.find({}, {"_id": 0}).sort("_id", -1).limit(limit)
    ]
