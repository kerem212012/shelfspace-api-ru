from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class BookBase(SQLModel):
    title: str = Field(index=True)
    author: str = Field(index=True)
    finished: bool = Field(default=False, index=True)


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    added_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BookCreate(BookBase):
    pass


class BookUpdate(SQLModel):
    title: str | None = Field(default=None, index=True)
    author: str | None = Field(default=None, index=True)
    finished: bool | None = Field(default=None, index=True)


class BookPublic(BookBase):
    id: int
    added_on: datetime
