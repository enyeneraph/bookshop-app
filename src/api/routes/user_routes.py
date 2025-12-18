from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api.schemas import UserBase, UserInDb, UserPublic, UserCreate
from api.app_depends import get_repository
from api.repositories import UserRepo
from api.repositories import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from api.auth import get_current_user

router = APIRouter(prefix="/user", tags=["Users"])

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.get("/", response_model=UserPublic)
async def view_users(user_repo:UserRepo= Depends(get_repository(UserRepo)), current_user: UserInDb = Depends(get_current_user)):
    users = await user_repo.get_users()
    return users

@router.post("/", response_model=UserInDb)
async def register(user: UserCreate, user_repo:UserRepo= Depends(get_repository(UserRepo))):
    users = await user_repo.register(user)
    return users

@router.delete("/{user_id}", response_model=dict)
async def delete(user_id:int, user_repo:UserRepo= Depends(get_repository(UserRepo)), current_user: UserInDb = Depends(get_current_user)):
    response = await user_repo.delete_user(user_id)
    if not response:
        raise HTTPException(status_code=404, detail=f'No User With book_id:{user_id} Was Found')
    return response

@router.get("/current user")
async def view_current_user(token:str = Depends(oauth2scheme), current_user: UserInDb = Depends(get_current_user)):
    return current_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user_repo:UserRepo= Depends(get_repository(UserRepo))):
    response = await user_repo.login(email=form_data.username, password=form_data.password)
    return response