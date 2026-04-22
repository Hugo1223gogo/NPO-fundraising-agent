import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI not found in .env")

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)

db = client["careerops_agent"]
collection = db["interactions"]


def test_connection():
    client.admin.command("ping")
    return "MongoDB connection successful"


def save_interaction(data: dict):
    result = collection.insert_one(data)
    return str(result.inserted_id)


def find_interactions_by_person(person_name: str):
    results = list(
        collection.find(
            {"person_name": {"$regex": f"^{person_name}$", "$options": "i"}},
            {"_id": 0}
        )
    )
    return results


def get_all_interactions():
    return list(collection.find({}, {"_id": 0}))
    
