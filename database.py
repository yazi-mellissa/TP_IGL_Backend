from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.orm.session import Session
from fastapi import Depends
from utils.Creds import DatabaseCreds

engine = create_engine(DatabaseCreds["Link"],
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_next_id(table_name : str, id_name : str, db : Session):
    req = text(f"SELECT MAX('{id_name}') FROM {table_name}")
    ID = db.execute(req).scalar() or 0
    return ID + 1