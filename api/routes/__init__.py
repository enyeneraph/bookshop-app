from fastapi import APIRouter
from routes.book_routes import router as book_router
from routes.order_routes import router as order_router
from routes.inventory_routes import router as inventory_router
from routes.user_routes import router as user_router

router = APIRouter()

router.include_router(book_router)
router.include_router(order_router)
router.include_router(inventory_router)
router.include_router(user_router)