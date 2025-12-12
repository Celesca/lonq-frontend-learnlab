from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "places.db")
DB_FILE = os.path.abspath(DB_FILE)
DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(DATABASE_URL, echo=False)

# Ensure parent directory exists so SQLite file can be created
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
