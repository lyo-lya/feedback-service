import pytest
from fastapi.testclient import TestClient
from app.main import app


# ---------- FAKE DB ----------
class FakeResult:
    def fetchone(self):
        return None

    def __iter__(self):
        return iter([])


class FakeConnection:
    def execute(self, *args, **kwargs):
        return FakeResult()

    def commit(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


def fake_connect():
    return FakeConnection()


# ---------- FIXTURE ----------
@pytest.fixture
def client(monkeypatch):
    """
    Clean isolated test client for every test
    """

    import app.main as main

    # patch DB connection safely
    monkeypatch.setattr(main.engine, "connect", fake_connect)

    return TestClient(app)