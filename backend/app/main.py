"""FastAPI app: one WebSocket endpoint that connects browsers to the current Session."""
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .ai_player import StubAI
from .config import load_config
from .session import Session

logging.basicConfig(level=logging.INFO)

app = FastAPI()
cfg = load_config()   # read config.yml once at startup (so: restart after editing it)
ai = StubAI()         # step (c): replaced by the Gemini player
current = None        # the one live session


def get_session() -> Session:
    """Return the live session, or start a fresh one if there is none or the last one is over."""
    global current
    if current is None or current.over:
        current = Session(cfg, ai)
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
