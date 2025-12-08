from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class OrderBase(BaseModel):
    book_id: int
    price: int
    count: int
    date: datetime

class OrdersInDb(OrderBase):
    id: int

    class Config:
        from_attributes = True

class OrdersPublic(BaseModel):
    total_count: int
    data: List[OrdersInDb]