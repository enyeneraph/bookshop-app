from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import InventoryBase, InventoryInDb, InventoryPublic
from app_depends import get_repository
from repositories import InventoryRepo
from auth import get_current_user
from schemas import UserInDb

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/", response_model=InventoryPublic)
async def view(inventory_repo:InventoryRepo= Depends(get_repository(InventoryRepo)), current_user: UserInDb = Depends(get_current_user)):
    inventory = await inventory_repo.get_inventory()
    return inventory

@router.post("/", response_model=InventoryInDb)
async def add(inventory: InventoryBase, inventory_repo:InventoryRepo= Depends(get_repository(InventoryRepo)), current_user: UserInDb = Depends(get_current_user)):
    inventory = await inventory_repo.add_inventory(inventory)
    return inventory

@router.delete("/{id}")
async def delete(id: int, inventory_repo:InventoryRepo= Depends(get_repository(InventoryRepo)), current_user: UserInDb = Depends(get_current_user)):
    response = await inventory_repo.delete_inventory(id)
    # if not response:
    #     raise HTTPException(status_code=404, detail=f'No Book With book_id:{id} Was Found')
    return response