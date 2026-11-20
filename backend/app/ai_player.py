"""AI players.

The session only needs two methods from an AI object:
    await ai.reply(player_id, messages, round_no)  -> str or None (None = stay silent)
    await ai.vote(player_id, messages)             -> "A", "B" or "C"

StubAI is a placeholder with canned lines and random votes.
In step (c) we replace it with a Gemini-based class that has the same two methods.
"""
import random

from .config import PLAYER_IDS

LINES = [
    "Who wants to start? I think we should pick someone who listens well.",
    "I am not sure yet. What do the others think?",
    "I could do it, but I am happy to support someone else too.",
    "Let's each say one reason, then decide.",
    "Good point. I am still thinking about it.",
]


class StubAI:
    async def reply(self, player_id, messages, round_no):
        return random.choice(LINES)

    async def vote(self, player_id, messages):
        return random.choice(PLAYER_IDS)
