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

    def __repr__(self):
        return f"(id={self.id},title={self.title}, author={self.author}, genre={self.genre}, year={self.year})"


class BookInventory(Base):
    __tablename__ = "book_inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    count: Mapped[int]
    total_count: Mapped[int]
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

    def __repr__(self):
        return f"(id={self.id},first_name={self.first_name}, last_name={self.last_name}, mail={self.mail}, role={self.role})"
    

class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int]
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[str]

    user: Mapped['Users'] = relationship(back_populates="orders")

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