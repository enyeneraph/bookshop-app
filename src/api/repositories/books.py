from api.repositories.base import BaseRepository
from sqlalchemy import select, insert, or_
from api.models import Book
from api.schemas import BookCreate, BookPublic, BookinDB
from sqlalchemy.sql import func
from fastapi import HTTPException
import sqlalchemy
from api.models import BookMetaData, Orders

class BookRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db)

    async def get_all_books(self, page:int, page_limit:int):
        offset = (page - 1) * page_limit
        query = select(Book).offset(offset).limit(page_limit)
        books = self.db.execute(query).scalars().all()
        count_query = select(func.count()).select_from(Book)
        count = self.db.execute(count_query).one()
        books = [BookinDB.model_validate(book) for book in books]
        result = BookPublic(total_count=count[0], data=books, 
                            page_limit=page_limit, page=page)
        return result
    
    async def search_books(self, search_query:str, page:int, page_limit:int):
        search_query = f"%{search_query}%"
        offset = (page - 1) * page_limit
        query = select(Book).where(or_(Book.title.ilike(search_query), 
                                       Book.author.ilike(search_query)))
        count_query = select(func.count()).select_from(query)
        count = self.db.execute(count_query).one()

        query = query.offset(offset).limit(page_limit)
        books = self.db.execute(query).scalars().all()

        books = [BookinDB.model_validate(book) for book in books]
        result = BookPublic(total_count=count[0], data=books, 
                            page_limit=page_limit, page=page)
        return result
    

    async def get_book_by_id(self, book_id:int):
        query = select(Book).where(Book.id == book_id)
        book = self.db.execute(query)
        try:
            books = book.scalars().one()
            return books
        except sqlalchemy.exc.NoResultFound:
            return None
    
    async def create_book(self, book:BookCreate):
        values = book.model_dump(exclude_none=True)
        book = Book(**values)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book
    
    async def delete_book(self, book_id:int):
        book = self.db.get(Book, book_id)
        self.db.delete(book)
        self.db.commit()
        return {'status':'success', 'message':'Data successfully deleted'}

    async def update_book_count(self, order_id: int, book_id: int):
        order = select(Orders).where(Orders.id == order_id)
        order = self.db.execute(order).scalar_one()
        if order is None:
           return {f'No Order with ID {order_id} found'}
        query = select(BookMetaData).where(BookMetaData.book_id == book_id)
        metadata = self.db.execute(query).scalar_one()
        metadata.total_count = order.count + metadata.total_count
        self.db.commit()
        self.db.refresh(order)
        return order
    
    async def reduce_book_count(self, book_id: int, count: int):
        metadata = select(BookMetaData).where(BookMetaData.book_id == book_id)
        metadata = self.db.execute(metadata).scalar_one()
        print(metadata)
        if metadata is None:
            metadata = BookMetaData(book_id = book_id, total_count = 0)
            self.db.add(metadata)
        metadata.total_count = metadata.total_count - count
        self.db.commit()
        self.db.refresh(metadata)
        return metadata