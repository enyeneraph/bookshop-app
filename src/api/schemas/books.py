from pydantic import BaseModel
from typing import List

class BookBase(BaseModel):
    title: str
    author: str
    year: int
    genre: str

class BookCreate(BookBase):
    pass

class BookinDB(BookBase):
    id: int

    class Config:
        from_attributes = True

class BookPublic(BaseModel):
    total_count: int
    page: int
    page_limit: int
    data: List[BookinDB]
