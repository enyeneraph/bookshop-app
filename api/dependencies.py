from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends
from repositories import BaseRepository

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_repository(repo_type: BaseRepository):
    def _get_repo(db:Session = Depends(get_db)):
        return repo_type(db)
    return _get_repo