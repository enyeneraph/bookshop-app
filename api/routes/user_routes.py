from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import UserBase, UserInDb, UserPublic
from dependencies import get_repository
from repositories import UserRepo

router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/", response_model=UserPublic)
async def view_users(user_repo:UserRepo= Depends(get_repository(UserRepo))):
    users = await user_repo.get_users()
    
    return users

@router.post("/", response_model=UserInDb)
async def register(user: UserBase, user_repo:UserRepo= Depends(get_repository(UserRepo))):
    users = await user_repo.register(user)
    return users

@router.delete("/{user_id}", response_model=dict)
async def delete(user_id:int, user_repo:UserRepo= Depends(get_repository(UserRepo))):
    response = await user_repo.delete_user(user_id)
    if not response:
        raise HTTPException(status_code=404, detail=f'No User With book_id:{user_id} Was Found')
    return response

# @ router.get("/")
# async def get_current_user(user_repo:UserRepo= Depends(get_repository(UserRepo))):
#     pass