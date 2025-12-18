from fastapi import APIRouter
from api.routes.book_routes import router as book_router
from api.routes.order_routes import router as order_router
from api.routes.inventory_routes import router as inventory_router
from api.routes.user_routes import router as user_router
from api.routes.cart import router as cart_router

router = APIRouter()

router.include_router(book_router)
router.include_router(order_router)
router.include_router(inventory_router)
router.include_router(user_router)
router.include_router(cart_router)