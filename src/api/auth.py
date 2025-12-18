from sqlalchemy import select, insert
from api.models import Users, Blacklist
from api.schemas import UserBase, UserInDb, UserPublic
from fastapi import FastAPI, Query, Path, status, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from api.config import *
from jose import JWTError, jwt, ExpiredSignatureError
# from app_depends import get_db
from api.database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

pwd_context = PasswordHash.recommended()

def hash_password(password):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password )

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def verify_access_token_validity(token:str, db:Database):
    try:
        value = db.execute(select(Blacklist).where(Blacklist.tokens == token)).scalar_one()
    except Exception:
        value = None

    return value

async def get_current_user(token:str = Depends(oauth2scheme), db:Database = Depends(get_db)):
    try:
        token_check = await verify_access_token_validity(token, db)
        if token_check:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = token
        data = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
        email = data['sub']

        existing_user = db.execute(select(Users).where(Users.mail == email))
        existing_user = existing_user.scalar_one()
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return UserInDb.model_validate(existing_user)
    except ExpiredSignatureError:
        raise  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"})