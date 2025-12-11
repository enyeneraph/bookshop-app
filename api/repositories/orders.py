from repositories.base import BaseRepository
from sqlalchemy import select, insert
from models.books import Orders, Users, Cart
from schemas import OrdersInDb, OrdersPublic, OrderBase,UserInDb
from sqlalchemy.sql import func
import sqlalchemy
from repositories import BookRepository

class OrderRepo(BaseRepository):
    def __init__(self, db):
        super().__init__(db)
        self.book_repo = BookRepository(db)

    async def get_all_orders(self, user_id: int):
        query = select(Orders).where(Orders.user_id == user_id)
        orders = self.db.execute(query).scalars().all()
        count_query = select(func.count()).select_from(Orders)
        count = self.db.execute(count_query).one()
        orders = [OrdersInDb.model_validate(order) for order in orders]
        result = OrdersPublic(total_count=count[0], data=orders)
        return result

    async def add_order(self, user_id: int, order: OrderBase):
            try:
                values = order.model_dump(exclude_none=True)
                values.update({"user_id": user_id})

                query = select(Cart).filter(Cart.user_id == user_id, Cart.checked_out == False)
                cart_data = self.db.execute(query).scalar_one()
                values.update({"cart_id": cart_data.id})
                order = Orders(**values)
            except sqlalchemy.exc.NoResultFound:
                cart_data = Cart(user_id= user_id, price=0)
                order = Orders(**values)
                order.cart = cart_data
            self.db.add(order)
            await self.book_repo.reduce_book_count(order.book_id, order.count)
            await self.book_repo.update_price(user_id=user_id, price=order.price)
            self.db.commit()
            self.db.refresh(order)
            order = OrdersInDb.model_validate(order)
            return order
        # except Exception as e:
            # return None
            
    async def delete_order(self, order_id: int, user_id: int):
        order = self.db.query(Orders).filter(Orders.id == order_id, Orders.user_id == user_id).one()
        book_id = order.book_id
        count = order.count
        await self.book_repo.update_book_count(count=count, book_id=book_id)
        self.db.delete(order)
        self.db.commit()
        return {'status':'success', 'message':'Data successfully deleted'}
    