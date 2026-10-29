from sqlalchemy import create_engine 
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker,declarative_base

import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Database_URL is missing from .env")
engine = create_engine(DATABASE_URL,pool_pre_ping = True)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind=engine
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

Base = declarative_base()