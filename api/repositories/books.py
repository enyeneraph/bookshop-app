from repositories.base import BaseRepository
from sqlalchemy import select, insert
from models import Book
from schemas import BookCreate, BookPublic, BookinDB
from sqlalchemy.sql import func

class BookRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db)

    async def get_all_books(self):
        query = select(Book)
        books = self.db.execute(query).scalars().all()
        count_query = select(func.count()).select_from(Book)
        count = self.db.execute(count_query).one()
        books = [BookinDB.model_validate(book) for book in books]
        result = BookPublic(total_count=count[0], data=books)
        return result

    async def get_book_by_id(self, book_id:int):
        query = select(Book).where(Book.id == book_id)
        book = self.db.execute(query).scalars().one()
        return book
    
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

