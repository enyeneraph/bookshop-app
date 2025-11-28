from dotenv import dotenv_values
from dotenv import dotenv_values
from databases import Database

config = dotenv_values("c:/Users/OWNER/Desktop/bookshop-app/.env")

POSTGRES_DB = config["POSTGRES_DB"]
POSTGRES_SERVER = config["POSTGRES_SERVER"]
POSTGRES_PORT = config["POSTGRES_PORT"]
POSTGRES_USER = config["POSTGRES_USER"]
POSTGRES_PASSWORD = config["POSTGRES_PASSWORD"]
SECRET_KEY = config['SECRET_KEY']
ALGORITHM = config['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = config['ACCESS_TOKEN_EXPIRE_MINUTES']

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"