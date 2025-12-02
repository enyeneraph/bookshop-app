from repositories.base import BaseRepository
from sqlalchemy import select, insert
from models.books import Orders, Users
from schemas import OrdersInDb, OrdersPublic, OrderBase,UserInDb
from sqlalchemy.sql import func
from fastapi import HTTPException, Depends
import sqlalchemy
from auth import get_current_user
from repositories import BookRepository

class OrderRepo(BaseRepository):
    def __init__(self, db):
        super().__init__(db)
        self.book_repo = BookRepository(db)

    async def get_all_orders(self, current_user: UserInDb = Depends(get_current_user)):
        query = select(Orders).filter(Orders.user_id == current_user.id)
        orders = self.db.execute(query).scalars().all()
        count_query = select(func.count()).select_from(Orders)
        count = self.db.execute(count_query).one()
        orders = [OrdersInDb.model_validate(orders) for order in orders]
        result = OrdersPublic(total_count=count[0], data=orders)
        return result

    async def add_order(self, order: OrderBase, current_user: UserInDb = Depends(get_current_user)):
        try:
            query = select(Users).where(Users.id == current_user.id)
            result = self.db.execute(query)
            values = order.model_dump(exclude_none=True)
            order = Orders(**values)
            self.db.add(order)
            # await self.book_repo.reduce_book_count(book_id, count)
            self.db.commit()
            self.db.refresh(order)
            return order
        except sqlalchemy.exc.NoResultFound:
            return None
        except Exception:
            return None
    
    async def delete_order(self, id: int, current_user: UserInDb = Depends(get_current_user)):
        order = self.db.query(Orders).filter(Orders.id == id, Orders.user_id == current_user.id)
        self.db.delete(order)
        select(Orders).where(Orders.id  == id)
        # await self.book_repo.update_book_count(order.id, order.count)
        self.db.commit()
        return {'status':'success', 'message':'Data successfully deleted'}
    


# order adds with new cart record and stores its id... if cart not closed new order uses the same cart id until closed
# total count should reduce when order is deleted
# book search by params
#pagenation