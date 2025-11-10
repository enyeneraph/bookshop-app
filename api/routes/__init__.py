from fastapi import APIRouter
from routes.book_routes import router as book_router

router = APIRouter()

router.include_router(book_router)