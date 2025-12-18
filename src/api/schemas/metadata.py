from pydantic import BaseModel

class MetaBase(BaseModel):
    id: int
    book_id: int
    total_count: int