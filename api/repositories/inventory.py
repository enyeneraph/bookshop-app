from repositories.base import BaseRepository
from sqlalchemy import select, insert
from models.books import BookInventory
from schemas import InventoryPublic, InventoryInDb, InventoryBase,UserInDb
from sqlalchemy.sql import func
from repositories.users import get_current_user
from fastapi import Depends
from models import BookMetaData
from repositories import BookRepository

class InventoryRepo(BaseRepository):
    def __init__(self, db):
        super().__init__(db)
        self.book_repo = BookRepository(db)

    async def get_inventory(self, current_user: UserInDb = Depends(get_current_user)):
        query = select(BookInventory)
        inventory = self.db.execute(query).scalars().all()
        count_query = select(func.count()).select_from(BookInventory)
        count = self.db.execute(count_query).one()
        inventory = [InventoryInDb.model_validate(i) for i in inventory]
        result = InventoryPublic(inventory_count=count[0], data=inventory)
        return result
    
    async def add_inventory(self, add: InventoryBase):
        values = add.model_dump(exclude_none=True)
        add = BookInventory(**values)
        self.db.add(add)
        await self.book_repo.update_book_count(book_id=add.book_id, count=add.count)
        self.db.commit()
        self.db.refresh(add)
        return add

    async def delete_inventory(self, id: int):
        item = self.db.get(BookInventory, id)
        self.db.delete(item)
        self.db.commit()
        return {'status':'success', 'message':'Data successfully deleted'}
 