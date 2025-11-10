from  database import Base, engine
from sqlalchemy.orm import Mapped
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from datetime import datetime, timezone
from typing import List

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    genre: Mapped[str]
    price: Mapped[int] 
    
    book_inventory: Mapped[List['BookInventory']] = relationship(back_populates="book")

    def __repr__(self):
        return f"Book: {self.title}"


class BookInventory(Base):
    __tablename__ = "book_inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    count: Mapped[int]
    total_count: Mapped[int]
    price: Mapped[int]

    book: Mapped['Book'] = relationship(back_populates="book_inventory")


