from typing import Annotated

from sqlmodel import create_engine, Session, SQLModel
from fastapi import Depends

DATABASE_URL = "sqlite:///shelfspace.db"
# Для PostgreSQL:
# DATABASE_URL = "postgresql://user:pass@localhost/mydb"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False},)  # echo=True логирует SQL

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]