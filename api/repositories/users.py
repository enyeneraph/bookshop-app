from repositories.base import BaseRepository
from sqlalchemy import select, insert
from models.books import Users
from schemas import UserBase, UserInDb, UserPublic
from sqlalchemy.sql import func
from fastapi import HTTPException, status

class UserRepo(BaseRepository):
    def __init__(self, db):
        super().__init__(db)

    async def register(self, user: UserBase):
        values = user.model_dump(exclude_none= True)
        values["role"] = user.role.value
        user = Users(**values)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    async def delete_user(self, id: int):
        user = self.db.get(Users, id)
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
        