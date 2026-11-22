"""FastAPI app: one WebSocket endpoint that connects browsers to the current Session."""
import logging
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .ai_player import make_ai
from .config import load_config
from .db import make_store
from .session import Session

logging.basicConfig(level=logging.INFO)
load_dotenv(Path(__file__).resolve().parents[2] / ".env")  # local runs: read GEMINI_API_KEY from .env in the repo root

app = FastAPI()
cfg = load_config()   # read config.yml once at startup (so: restart after editing it)
ai = make_ai(cfg)     # Gemini if GEMINI_API_KEY is set, else the placeholder AI
store = make_store()  # MongoDB if MONGO_URL is set, else None
current = None        # the one live session


def get_session() -> Session:
    """Return the live session, or start a fresh one if there is none or the last one is over."""
    global current
    if current is None or current.over:
        current = Session(cfg, ai, on_finish=store.save_session if store else None)
    return current


@app.get("/health")
def health():
    return {"ok": True}


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    session = get_session()
    pid = session.join(ws.send_json)
    if pid is None:  # experiment already running or full
        await ws.send_json({"type": "busy"})
        await ws.close()
        return
    await ws.send_json({"type": "joined", "you": pid})  # tell the player their letter first ...
    session.maybe_start()                               # ... then start if all humans are here
    try:
        while True:
            msg = await ws.receive_json()               # wait for chat / vote messages
            await session.handle(pid, msg)
    except WebSocketDisconnect:
        pass
    finally:
        session.leave(pid)
