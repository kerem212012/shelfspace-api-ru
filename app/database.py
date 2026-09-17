import os
from typing import Annotated

from sqlmodel import create_engine, Session, SQLModel
from fastapi import Depends

DATABASE_URL = "sqlite:///shelfspace.db"


def create_db_engine(database_url: str | None = None):
    url = database_url or os.getenv("DATABASE_URL", DATABASE_URL)
    return create_engine(url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(create_db_engine())

def get_session():
    with Session(create_db_engine()) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]