from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.books import BookCreate, BookinDB, BookPublic
from app_depends import get_repository
from repositories import BookRepository
import sqlalchemy
from auth import get_current_user
from schemas import UserInDb

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=BookPublic)
async def list_books(book_repo:BookRepository= Depends(get_repository(BookRepository)), current_user: UserInDb = Depends(get_current_user)):
    books = await book_repo.get_all_books()
    return books

@router.get("/{book_id}", response_model=BookinDB)
async def get_book(book_id:int, book_repo:BookRepository= Depends(get_repository(BookRepository)), current_user: UserInDb = Depends(get_current_user)):
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
