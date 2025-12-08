from database import Base, engine
from sqlalchemy.orm import Mapped
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from datetime import datetime, timezone
from typing import List
from sqlalchemy import Enum as SQLAEnum
from schemas.users import Role

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    genre: Mapped[str]
    year: Mapped[int] 
    
    book_inventory: Mapped[List['BookInventory']] = relationship(back_populates="book")
    book_data: Mapped[List['BookMetaData']] = relationship(back_populates = "book")
    orders: Mapped['Orders'] = relationship(back_populates = "book")

    def __repr__(self):
        return f"(id={self.id},title={self.title}, author={self.author}, genre={self.genre}, year={self.year})"


class BookInventory(Base):
    __tablename__ = "book_inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    count: Mapped[int]
    price: Mapped[int]

    book: Mapped['Book'] = relationship(back_populates="book_inventory")


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    mail: Mapped[str]
    password: Mapped[str]
    role: Mapped[str]

    orders: Mapped[List["Orders"]] = relationship(back_populates="user")
    cart: Mapped["Cart"] = relationship(back_populates="users")

    def __repr__(self):
        return f"(id={self.id},first_name={self.first_name}, last_name={self.last_name}, mail={self.mail}, role={self.role})"
    

class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"))
    count: Mapped[int]
    price: Mapped[int]
    date: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped['Users'] = relationship(back_populates="orders")
    book: Mapped['Book'] = relationship(back_populates="orders")
    cart: Mapped['Cart'] = relationship(back_populates="orders")

    def __repr__(self):
        return f"(id={self.id},title={self.title}, user_id={self.user_id}, amount={self.amount}, date={self.date}, status={self.status})"
    

class BookMetaData(Base):
    __tablename__= "book_metadata"
    id: Mapped[int] = mapped_column(primary_key = True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    total_count: Mapped[int]

    book: Mapped['Book'] = relationship(back_populates="book_data")

# Base.metadata.create_all(engine)

class Blacklist(Base):
    __tablename__= "blacklist"
    id: Mapped[int] = mapped_column(primary_key=True)
    tokens: Mapped[str]


class Cart(Base):
    __tablename__= "cart"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    checkout_date: Mapped[datetime]= mapped_column(server_default=func.now())
    checked_out: Mapped[bool] = mapped_column(default=False)
    price: Mapped[int]

    users: Mapped['Users'] = relationship(back_populates="cart")
    orders: Mapped['Orders'] = relationship(back_populates="cart")

    def __repr__(self):
        return f'id={self.id}, user_id={self.user_id}, checkout_date={self.checkout_date}, checked_out={self.checked_out}, price={self.price}'