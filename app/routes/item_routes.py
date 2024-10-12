from fastapi import APIRouter, HTTPException
from app.models.item_model import ItemCreate, ItemUpdate
from app.services.database import items_collection, item_helper
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/items")
async def create_item(item: ItemCreate):
    new_item = {**item.dict(), "insert_date": datetime.now()}
    result = await items_collection.insert_one(new_item)
    return {"id": str(result.inserted_id)}

@router.get("/items/{id}")
async def get_item(id: str):
    item = await items_collection.find_one({"_id": ObjectId(id)})
    if item:
        return item_helper(item)
    raise HTTPException(status_code=404, detail="Item not found")

@router.get("/items/filter")
async def filter_items(email: str = None, expiry_date: str = None, insert_date: str = None, quantity: int = None):
    query = {}
    if email:
        query["email"] = email
    if expiry_date:
        query["expiry_date"] = {"$gte": datetime.strptime(expiry_date, "%Y-%m-%d")}
    if insert_date:
        query["insert_date"] = {"$gte": datetime.strptime(insert_date, "%Y-%m-%d")}
    if quantity:
        query["quantity"] = {"$gte": quantity}
    
    items = await items_collection.find(query).to_list(100)
    return [item_helper(item) for item in items]

@router.put("/items/{id}")
async def update_item(id: str, item: ItemUpdate):
    updated_data = {k: v for k, v in item.dict().items() if v is not None}
    if updated_data:
        result = await items_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        if result.modified_count == 1:
            return {"msg": "Item updated successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{id}")
async def delete_item(id: str):
    result = await items_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"msg": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
