from api.repositories.base import BaseRepository
from sqlalchemy import select, insert
from api.models import MetaData, BookInventory, Book

class MetaRepo(BaseRepository):
    def __init__(self, db):
        super().__init__(db)

    async def add_count(self, book_id: int, data: MetaData):
        cur_total = select(Book).where(Book.id == book_id)
        self.db.execute(cur_total)
        self.db.refresh(cur_total)
        total = select


        

    async def subtract_count(self):

        pass
