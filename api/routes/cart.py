from fastapi import APIRouter, Depends, HTTPException
from schemas import CartBase, CartInDb, CartPublic
from app_depends import get_repository
from repositories import CartRepo
from auth import get_current_user
from schemas import UserInDb

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=CartPublic)
async def view_cart(cart_repo:CartRepo= Depends(get_repository(CartRepo)), current_user: UserInDb = Depends(get_current_user)):
    cart = await cart_repo.cart()
    return cart

@router.post("/{cart_id}", response_model=CartInDb)
async def checkout_cart(cart_id: int, cart: CartBase, cart_repo:CartRepo= Depends(get_repository(CartRepo)), current_user: UserInDb = Depends(get_current_user)):
    cart = await cart_repo.checkout(cart_id=cart_id, car=cart)
    if not cart:
        raise HTTPException(status_code=404, detail=f'No Cart With id:{cart_id} Was Found')
    return cart