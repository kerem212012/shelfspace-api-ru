from fastapi import FastAPI

app = FastAPI(title="ShelfSpace API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Add SQLModel tables, a session dependency, and persistent book routes.
