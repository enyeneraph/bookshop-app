from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Role(Enum):
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    first_name: str
    last_name: str
    mail: EmailStr
    password: str
    role: Optional[Role] = "user"

class UserInDb(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    total_count: int
    data: List[UserInDb]