from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_all_tables
from models import BookMetaData
import uvicorn
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables")
    create_all_tables()
    yield
    print("⚡ App is shutting down")


app = FastAPI(title="Book shop app", lifespan=lifespan)
app.include_router(router=router)

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True) 