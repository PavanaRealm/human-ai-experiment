"""Tests for the AI player code. A fake client stands in for Gemini, so no key and no internet are needed."""
import asyncio
from types import SimpleNamespace

import pytest

from app.ai_player import GeminiAI, StubAI, clean_reply, make_ai, parse_vote, transcript
from app.config import Config


class FakeModels:
    def __init__(self, text, delay=0):
        self.text, self.delay, self.calls = text, delay, []

    async def generate_content(self, model, contents, config):
        self.calls.append({"model": model, "contents": contents, "config": config})
        await asyncio.sleep(self.delay)
        return SimpleNamespace(text=self.text)


def fake_client(text, delay=0):
    return SimpleNamespace(aio=SimpleNamespace(models=FakeModels(text, delay)))


MESSAGES = [
    {"round": 1, "from": "A", "text": "I think B is calm."},
    {"round": 1, "from": "C", "text": "Why B?"},
]


# ---------- helpers ----------

@pytest.mark.parametrize("answer, expected", [
    ("B", "B"), ("b.", "B"), ("(C)", "C"), ("  A\n", "A"),
    ("I vote for Player C", "C"),
    ("", None), (None, None), ("I cannot decide", None), ("D", None),
])
def test_parse_vote(answer, expected):
    assert parse_vote(answer) == expected


def test_clean_reply():
    assert clean_reply('Player B: "Sounds good to me."') == "Sounds good to me."
    assert clean_reply("  plain text  ") == "plain text"
    assert clean_reply(None) == ""


def test_transcript():
    assert transcript(MESSAGES) == "Player A: I think B is calm.\nPlayer C: Why B?"
    assert "Nobody" in transcript([])


# ---------- GeminiAI with a fake client ----------

def test_reply_sends_the_chat_and_a_persona():
    client = fake_client('Player B: "Fair point, I could do it."')
    ai = GeminiAI("key", "my-model", rounds=2, client=client)
    text = asyncio.run(ai.reply("B", MESSAGES, round_no=1))

    assert text == "Fair point, I could do it."          # prefix and quotes removed
    call = client.aio.models.calls[0]
    assert call["model"] == "my-model"
    assert "Player A: I think B is calm." in call["contents"]
    system = call["config"].system_instruction
    assert "You are Player B" in system and "Player A" in system and "Player C" in system
    assert "round 1 of 2" in system


def test_empty_reply_means_stay_silent():
    ai = GeminiAI("key", "m", rounds=2, client=fake_client("   "))
    assert asyncio.run(ai.reply("B", MESSAGES, 1)) is None


def test_vote_returns_a_letter_or_none():
    assert asyncio.run(GeminiAI("k", "m", 2, client=fake_client("C")).vote("A", MESSAGES)) == "C"
    assert asyncio.run(GeminiAI("k", "m", 2, client=fake_client("hmm")).vote("A", MESSAGES)) is None


def test_slow_gemini_call_is_cancelled():
    ai = GeminiAI("key", "m", rounds=2, timeout=0.05, client=fake_client("hi", delay=1))
    with pytest.raises(asyncio.TimeoutError):
        asyncio.run(ai.reply("B", MESSAGES, 1))


# ---------- choosing the implementation ----------

def make_cfg(participants):
    return Config(participants=participants, rounds=2, chat_seconds=1, vote_seconds=1, feedback_seconds=0,
                  min_wait_seconds=0, ai_model="x", ai_reply_delay=(1, 2))


def test_make_ai(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert make_ai(make_cfg(["human", "human", "human"])) is None            # no AI needed
    assert isinstance(make_ai(make_cfg(["human", "human", "ai"])), StubAI)   # no key -> placeholder
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    assert isinstance(make_ai(make_cfg(["human", "human", "ai"])), GeminiAI)
