"""Save finished sessions to MongoDB (optional: only if MONGO_URL is set)."""
import logging
import os

from pymongo import AsyncMongoClient

log = logging.getLogger("db")


class Store:
    def __init__(self, url: str):
        # Fail after 3 s if MongoDB is not reachable, instead of the default 30 s.
        client = AsyncMongoClient(url, serverSelectionTimeoutMS=3000)
        self.sessions = client["experiment"]["sessions"]

    async def save_session(self, record: dict) -> None:
        await self.sessions.insert_one(record)


def make_store():
    """A Store if MONGO_URL is set, otherwise None (the experiment then just does not save)."""
    url = os.getenv("MONGO_URL")
    if not url:
        log.warning("MONGO_URL is not set: finished sessions will NOT be saved")
        return None
    log.info("Finished sessions are saved to MongoDB")
    return Store(url)
