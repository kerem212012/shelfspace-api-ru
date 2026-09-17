from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from app.database import create_db_engine, get_session
from app.main import app


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    monkeypatch.setenv("DATABASE_URL", database_url)
    test_engine = create_db_engine(database_url)
    SQLModel.metadata.create_all(test_engine)

    def get_test_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_books_survive_multiple_requests(client: TestClient) -> None:
    dune = client.post(
        "/books",
        json={"title": "Dune", "author": "Frank Herbert", "finished": False},
    )
    foundation = client.post(
        "/books",
        json={"title": "Foundation", "author": "Isaac Asimov", "finished": False},
    )
    assert dune.status_code == 201
    assert foundation.status_code == 201
    dune_id = dune.json()["id"]
    foundation_id = foundation.json()["id"]

    assert client.get(f"/books/{dune_id}").json()["title"] == "Dune"
    assert client.patch(f"/books/{dune_id}", json={"finished": True}).json() == {
        **dune.json(),
        "finished": True,
    }
    assert [book["id"] for book in client.get("/books?finished=true").json()] == [dune_id]
    assert [book["id"] for book in client.get("/books?search=asimov").json()] == [foundation_id]
    assert [book["id"] for book in client.get("/books?offset=1&limit=1").json()] == [foundation_id]

    assert client.delete(f"/books/{dune_id}").status_code == 204
    assert client.get(f"/books/{dune_id}").status_code == 404
    assert client.get(f"/books/{foundation_id}").status_code == 200
