from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(engine)

def create_all_tables():
    Base.metadata.create_all(bind=engine)

