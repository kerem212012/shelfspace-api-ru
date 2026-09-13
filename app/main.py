from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager

from app.database import create_db_and_tables, SessionDep


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

# Add SQLModel tables, a session dependency, and persistent book routes.
