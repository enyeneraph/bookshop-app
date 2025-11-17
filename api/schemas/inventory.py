from pydantic import BaseModel
from typing import Optional, List
from schemas.books import BookBase
from datetime import datetime

class InventoryBase(BaseModel):
    book_id: int
    date: datetime
    count: int
    total_count: int
    price: int
    
class InventoryInDb(InventoryBase):
    id: int

    class Config:
        from_attributes = True
    
class InventoryPublic(BaseModel):
    inventory_count: int
    data: List[InventoryInDb]