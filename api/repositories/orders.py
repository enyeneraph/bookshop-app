from repositories.base import BaseRepository
from sqlalchemy import select, insert
from models.books import Orders, Users
from schemas import OrdersInDb, OrdersPublic, OrderBase
from sqlalchemy.sql import func
from fastapi import HTTPException
import sqlalchemy

class OrderRepo(BaseRepository):
    def __init__(self, db):
        super().__init__(db)

    async def get_all_orders(self):
        query = select(Orders)
        orders = self.db.execute(query).scalars().all()
        count_query = select(func.count()).select_from(Orders)
        count = self.db.execute(count_query).one()
        orders = [OrdersInDb.model_validate(orders) for order in orders]
        result = OrdersPublic(total_count=count[0], data=orders)
        return result
    
    async def add_order(self, order: OrderBase):
        try:
            query = select(Users).where(Users.id == Orders.user_id)
            result = self.db.execute(query)
            # print(result)
            # if result.first():
            #     print(1)
            values = order.model_dump(exclude_none=True)
            order = Orders(**values)
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)
            return order
        except sqlalchemy.exc.NoResultFound:
            return None
        except Exception:
            return None
    
    async def delete_order(self, id: int):
        order = self.db.get(Orders, id)
        self.db.delete(order)
        self.db.commit()
        return {'status':'success', 'message':'Data successfully deleted'}