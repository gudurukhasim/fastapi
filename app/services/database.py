from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
db = client["fastapi_crud_mongo"]

items_collection = db.get_collection("items")
clockin_collection = db.get_collection("clockin_records")

# Utility function to format MongoDB data to Python dict
def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "item_name": item["item_name"],
        "quantity": item["quantity"],
        "expiry_date": item["expiry_date"],
        "insert_date": item["insert_date"]
    }

def clockin_helper(clockin) -> dict:
    return {
        "id": str(clockin["_id"]),
        "email": clockin["email"],
        "location": clockin["location"],
        "insert_date_time": clockin["insert_date_time"]
    }
