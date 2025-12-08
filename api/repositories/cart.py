from repositories.base import BaseRepository
from sqlalchemy import select, insert
from models.books import Cart
from schemas import CartInDb, CartPublic, CartBase
from sqlalchemy.sql import func

class CartRepo(BaseRepository):
    def __init__(self, db):
        super().__init__(db)

    async def checkout(self, cart_id: int, car:CartBase):
        query = select(Cart).where(Cart.id == cart_id)
        cart = self.db.execute(query).scalar_one()
        if not cart:
            return None

        values = car.model_dump(exclude_none=True)
        carts = Cart(**values)

        cart.checked_out = carts.checked_out
        self.db.commit()
        self.db.refresh(cart)
        return cart
    
    async def cart(self):
        query = select(Cart)
        carts = self.db.execute(query).scalars().all()
        count_query = select(func.count()).select_from(Cart)
        count = self.db.execute(count_query).one()
        cart = [CartInDb.model_validate(cart) for cart in carts]
        result = CartPublic(total_count=count[0], data=cart)
        return result