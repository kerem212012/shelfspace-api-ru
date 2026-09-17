from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlmodel import select

from app.database import SessionDep, create_db_and_tables
from app.models import Book, BookCreate, BookPublic, BookUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="ShelfSpace API",lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/debug-session")
def debug(session: SessionDep):
    return {"session_created":True}


@app.post("/books", response_model=BookPublic, status_code=201)
def create_book(payload: BookCreate, session: SessionDep):
    book = Book.model_validate(payload)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.get("/books", response_model=list[BookPublic])
def list_books(
    session: SessionDep,
    finished: bool | None = None,
    search: str | None = None,
    offset: int = 0,
    limit: int = 100,
):
    statement = select(Book)
    if finished is not None:
        statement = statement.where(Book.finished == finished)
    if search is not None:
        search_pattern = f"%{search}%"
        statement = statement.where(
            Book.title.ilike(search_pattern) | Book.author.ilike(search_pattern)
        )
    statement = statement.order_by(Book.id).offset(offset).limit(limit)
    return session.exec(statement).all()


@app.get("/books/{book_id}", response_model=BookPublic)
def get_book(book_id: int, session: SessionDep):
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.patch("/books/{book_id}", response_model=BookPublic)
def update_book(book_id: int, payload: BookUpdate, session: SessionDep):
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book.sqlmodel_update(payload.model_dump(exclude_unset=True))
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, session: SessionDep):
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
