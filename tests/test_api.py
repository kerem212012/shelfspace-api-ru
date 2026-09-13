from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    # The finished app may expose an engine dependency or use an env-configured URL.
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")
    with TestClient(app) as test_client:
        yield test_client


def test_books_survive_multiple_requests(client: TestClient) -> None:
    created = client.post("/books", json={"title": "Dune", "author": "Frank Herbert", "finished": False})
    assert created.status_code == 201
    book_id = created.json()["id"]
    assert client.get(f"/books/{book_id}").json()["title"] == "Dune"
    assert client.patch(f"/books/{book_id}", json={"finished": True}).json()["finished"] is True
    assert client.get("/books?finished=true").json()[0]["id"] == book_id
    assert client.delete(f"/books/{book_id}").status_code == 204
