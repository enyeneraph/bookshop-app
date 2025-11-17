from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import InventoryBase, InventoryInDb, InventoryPublic
from dependencies import get_repository
from repositories import InventoryRepo

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/", response_model=InventoryPublic)
async def view(inventory_repo:InventoryRepo= Depends(get_repository(InventoryRepo))):
    inventory = await inventory_repo.get_inventory()
    return inventory

@router.post("/", response_model=InventoryInDb)
async def add(inventory: InventoryBase, inventory_repo:InventoryRepo= Depends(get_repository(InventoryRepo))):
    inventory = await inventory_repo.add_book(inventory)
    return inventory

@router.delete("/{id}", response_model=InventoryInDb)
async def delete(id: int, inventory_repo:InventoryRepo= Depends(get_repository(InventoryRepo))):
    response = await inventory_repo.delete_inventory(id)
    # if not response:
    #     raise HTTPException(status_code=404, detail=f'No Book With book_id:{id} Was Found')
    return response