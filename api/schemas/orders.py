from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Status(str,Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class OrderBase(BaseModel):
    title: str
    user_id: int
    amount: int
    date: datetime
    status: Optional[Status] = "pending"

class OrdersInDb(OrderBase):
    id: int

    class Config:
        from_attributes = True

class OrdersPublic(BaseModel):
    total_count: int
    data: List[OrdersInDb]