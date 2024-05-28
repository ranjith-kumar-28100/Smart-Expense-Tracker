from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
db_name = os.getenv("DB_NAME")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_name}.db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def create_database():
    Base.metadata.create_all(bind=engine)
