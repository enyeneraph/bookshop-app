from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import OrderBase, OrdersInDb, OrdersPublic
from app_depends import get_repository
from repositories import OrderRepo
from auth import get_current_user
from schemas import UserInDb

router = APIRouter(prefix="/order", tags=["Orders"])

@router.get("/", response_model=OrdersPublic)
async def view_orders(order_repo:OrderRepo= Depends(get_repository(OrderRepo)), current_user: UserInDb = Depends(get_current_user)):
    orders = await order_repo.get_all_orders()
    return orders

@router.post("/", response_model=OrdersInDb)
async def order_book(order: OrderBase, order_repo:OrderRepo= Depends(get_repository(OrderRepo)), current_user: UserInDb = Depends(get_current_user)):
    orders = await order_repo.add_order(order)
    if not orders:
        raise HTTPException(status_code=500, detail="Failed To Create Order")
    return orders

@router.delete("/{order_id}", response_model=dict)
async def delete(order_id:int, order_repo:OrderRepo= Depends(get_repository(OrderRepo)), current_user: UserInDb = Depends(get_current_user)):
    response = await order_repo.delete_order(order_id)
    if not response:
        raise HTTPException(status_code=404, detail=f'No Book With book_id:{order_id} Was Found')
    return response