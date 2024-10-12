from fastapi import APIRouter, HTTPException
from app.models.clockin_model import ClockInCreate, ClockInUpdate
from app.services.database import clockin_collection, clockin_helper
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/clock-in")
async def clock_in(clockin: ClockInCreate):
    new_clockin = {**clockin.dict(), "insert_date_time": datetime.now()}
    result = await clockin_collection.insert_one(new_clockin)
    return {"id": str(result.inserted_id)}

@router.get("/clock-in/{id}")
async def get_clock_in(id: str):
    clockin = await clockin_collection.find_one({"_id": ObjectId(id)})
    if clockin:
        return clockin_helper(clockin)
    raise HTTPException(status_code=404, detail="Clock-in record not found")

@router.get("/clock-in/filter")
async def filter_clock_in(email: str = None, location: str = None, insert_date_time: str = None):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_date_time:
        query["insert_date_time"] = {"$gte": datetime.strptime(insert_date_time, "%Y-%m-%d %H:%M:%S")}
    
    records = await clockin_collection.find(query).to_list(100)
    return [clockin_helper(record) for record in records]

@router.put("/clock-in/{id}")
async def update_clock_in(id: str, clockin: ClockInUpdate):
    updated_data = {k: v for k, v in clockin.dict().items() if v is not None}
    if updated_data:
        result = await clockin_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        if result.modified_count == 1:
            return {"msg": "Clock-in record updated successfully"}
    raise HTTPException(status_code=404, detail="Clock-in record not found")

@router.delete("/clock-in/{id}")
async def delete_clock_in(id: str):
    result = await clockin_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"msg": "Clock-in record deleted successfully"}
    raise HTTPException(status_code=404, detail="Clock-in record not found")
