from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClockInCreate(BaseModel):
    email: str
    location: str

class ClockInUpdate(BaseModel):
    email: Optional[str] = None
    location: Optional[str] = None
