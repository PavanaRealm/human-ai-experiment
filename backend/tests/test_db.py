import asyncio

from app import db
from app.config import parse_config
from app.session import Session


class FakeCollection:
    def __init__(self):
        self.saved = []

    async def insert_one(self, record):
        self.saved.append(record)


def test_make_store_without_url(monkeypatch):
    monkeypatch.delenv("MONGO_URL", raising=False)
    assert db.make_store() is None


def test_make_store_with_url(monkeypatch):
    monkeypatch.setenv("MONGO_URL", "mongodb://localhost:27017")
    assert isinstance(db.make_store(), db.Store)  # does not connect yet, so no server needed


def test_save_session_inserts_the_record():
    store = db.Store("mongodb://localhost:27017")
    store.sessions = FakeCollection()
    asyncio.run(store.save_session({"a": 1}))
    assert store.sessions.saved == [{"a": 1}]


def test_finished_session_is_saved_through_on_finish():
    """The Session calls on_finish with export() when it ends."""
    saved = []

    async def on_finish(record):
        saved.append(record)

    cfg = parse_config({"participants": ["human", "human", "human"], "rounds": 1, "chat_seconds": 0.01,
                        "vote_seconds": 0.01, "feedback_seconds": 0.01, "min_wait_seconds": 0,
                        "ai": {"model": "x", "reply_delay_seconds": [0, 0]}})
    session = Session(cfg, None, on_finish=on_finish)
    session.round_tallies = [{"A": 2, "B": 1, "C": 0}]
    asyncio.run(session._finish())
    assert len(saved) == 1
    assert saved[0]["result"]["winner"] == "A"
    assert saved[0]["participants"] == {"A": "human", "B": "human", "C": "human"}


def test_failing_database_does_not_break_the_session():
    async def on_finish(record):
        raise RuntimeError("database is down")

    cfg = parse_config({"participants": ["human", "human", "human"], "rounds": 1, "chat_seconds": 1,
                        "vote_seconds": 1, "feedback_seconds": 1, "min_wait_seconds": 0,
                        "ai": {"model": "x", "reply_delay_seconds": [0, 0]}})
    session = Session(cfg, None, on_finish=on_finish)
    session.round_tallies = [{"A": 1, "B": 0, "C": 0}]
    asyncio.run(session._finish())  # must not raise
    assert session.over
