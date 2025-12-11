from pydantic import BaseModel
from typing import List
from datetime import datetime

class CartBase(BaseModel):
    checkout_date: datetime
    checked_out: bool
    price: int

class CartInDb(CartBase):
    id: int

    class Config:
        from_attributes = True


class CartPublic(BaseModel):
    total_count: int
    data: List[CartInDb]