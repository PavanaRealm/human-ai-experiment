"""Test through the real WebSocket endpoint (FastAPI's TestClient), not just the Session class."""
from fastapi.testclient import TestClient

import app.main as main
from app.config import Config


def test_full_game_over_websocket(monkeypatch):
    cfg = Config(participants=["human", "ai", "ai"], rounds=2, chat_seconds=0.3, vote_seconds=5,
                 feedback_seconds=0.05, min_wait_seconds=0, ai_model="x", ai_reply_delay=(0.02, 0.05))
    monkeypatch.setattr(main, "cfg", cfg)
    monkeypatch.setattr(main, "current", None)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as ws:
            assert ws.receive_json() == {"type": "joined", "you": "A"}

            # a second browser while the game is running is turned away
            with client.websocket_connect("/ws") as ws2:
                assert ws2.receive_json() == {"type": "busy"}

            while True:
                msg = ws.receive_json()
                if msg["type"] == "phase" and msg["phase"] == "chat":
                    ws.send_json({"type": "chat", "text": "hello"})
                if msg["type"] == "phase" and msg["phase"] == "vote":
                    ws.send_json({"type": "vote", "target": "A"})
                if msg["type"] == "phase" and msg["phase"] == "result":
                    break

    assert msg["winner"] in ("A", "B", "C")
    assert sum(msg["totals"].values()) == 6   # 3 voters x 2 rounds
    assert len(msg["round_tallies"]) == 2
