from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.schemas.books import BookCreate, BookinDB, BookPublic
from api.app_depends import get_repository
from api.repositories import BookRepository
import sqlalchemy
from api.auth import get_current_user
from api.schemas import UserInDb

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=BookPublic)
async def list_books(page: int = 1,
                     page_limit: int = 20, 
                    book_repo:BookRepository= Depends(get_repository(BookRepository))):
                    # current_user: UserInDb = Depends(get_current_user)):
    books = await book_repo.get_all_books(page=page, page_limit=page_limit)
    return books

@router.get("/search", response_model=BookPublic)
async def search_book(search_query: str, 
                      page: int = 1,
                     page_limit: int = 20,
                     book_repo:BookRepository= Depends(get_repository(BookRepository)),
                    current_user: UserInDb = Depends(get_current_user)):
    books = await book_repo.search_books(search_query=search_query, 
                                         page=page, page_limit=page_limit)
    return books

@router.get("/{book_id}", response_model=BookinDB)
async def get_book(book_id:int,
                   book_repo:BookRepository= Depends(get_repository(BookRepository)), 
                   current_user: UserInDb = Depends(get_current_user)):
    book = await book_repo.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f'No Book With book_id:{book_id} Was Found')
    return book

@router.post("/", response_model=BookinDB)
async def create_book(book: BookCreate, book_repo:BookRepository= Depends(get_repository(BookRepository)), current_user: UserInDb = Depends(get_current_user)):
    book = await book_repo.create_book(book)
    return book
   
@router.delete("/{book_id}", response_model=dict)
async def delete(book_id:int, book_repo:BookRepository= Depends(get_repository(BookRepository)), current_user: UserInDb = Depends(get_current_user)):
    response = await book_repo.delete_book(book_id)
    return response
