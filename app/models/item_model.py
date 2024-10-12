from pydantic import BaseModel
from typing import Optional
from datetime import date

class ItemCreate(BaseModel):
    name: str
    email: str
    item_name: str
    quantity: int
    expiry_date: date

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    item_name: Optional[str] = None
    quantity: Optional[int] = None
    expiry_date: Optional[date] = None
