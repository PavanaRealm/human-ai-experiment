"""A tiny terminal client that acts like a human player. For testing the backend without the frontend.

Run one copy per human slot in config.yml:   python fake_player.py
"""
import asyncio
import json
import sys

import websockets

URL = sys.argv[1] if len(sys.argv) > 1 else "ws://localhost:8000/ws"


async def main():
    async with websockets.connect(URL) as ws:
        async for raw in ws:
            msg = json.loads(raw)
            print("<-", msg)
            if msg["type"] == "busy":
                break
            if msg["type"] == "phase" and msg["phase"] == "chat":
                await ws.send(json.dumps({"type": "chat", "text": "Hello, I think A would be a good choice."}))
            if msg["type"] == "phase" and msg["phase"] == "vote":
                await ws.send(json.dumps({"type": "vote", "target": "A"}))
            if msg["type"] == "phase" and msg["phase"] == "result":
                break


asyncio.run(main())
