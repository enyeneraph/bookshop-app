from api.repositories.base import BaseRepository
from sqlalchemy import select, insert
from api.models import Users, Blacklist
from api.schemas import UserBase, UserInDb, UserPublic, UserCreate
from sqlalchemy.sql import func
from fastapi import FastAPI, Query, Path, status, HTTPException, Depends, status
from api.config import *
from jose import JWTError, jwt, ExpiredSignatureError
import sqlalchemy
from api.auth import *


class UserRepo(BaseRepository):
    def __init__(self, db):
        super().__init__(db)

    async def register(self, user: UserCreate):
        try:
            existing_user = self.db.execute(select(Users).where(Users.mail == user.mail)).scalars().one()
        except sqlalchemy.exc.NoResultFound:
            existing_user = None
        try:
            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
            else:
                values = user.model_dump(exclude_none= True)
                values["role"] = user.role.value
                values["password"] =  hash_password(values["password"])
                user = Users(**values)
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
                return user
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Email already registered")
    
    async def delete_user(self, id: int):
        user = self.db.get(Users, id)
        if user is None:
            raise HTTPException(
            status_code=404,
            detail="User not found"
        )
        self.db.delete(user)
        self.db.commit()
        return {'status':'success', 'message':'Data successfully deleted'}

    async def get_users(self):
        query = select(Users)
        users = self.db.execute(query).scalars().all()
        count_query = select(func.count()).select_from(Users)
        count = self.db.execute(count_query).one()
        users = [UserInDb.model_validate(user) for user in users]
        result = UserPublic(total_count=count[0], data=users)
        return result
       
        
    async def login(self, email: str, password: str):
        user = self.db.execute(select(Users).where(Users.mail == email)).scalar_one()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        access_token = create_access_token(data={"sub": user.mail, "role": user.role})

        return {"access_token": access_token, "token_type": "bearer"}