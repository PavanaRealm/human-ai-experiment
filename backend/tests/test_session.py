import asyncio
import json

import pytest

from app.config import Config
from app.session import Session, decide_winner


def make_cfg(participants, min_wait=0, vote_seconds=5):
    return Config(participants=participants, rounds=2, chat_seconds=0.3, vote_seconds=vote_seconds,
                  feedback_seconds=0.05, min_wait_seconds=min_wait, ai_model="x", ai_reply_delay=(0.02, 0.05))


class FakeAI:
    """Always says the same thing and votes for B."""
    async def reply(self, pid, messages, round_no):
        return f"hi from {pid}"

    async def vote(self, pid, messages):
        return "B"


class BotHuman:
    """Pretends to be a browser: records what the server sends, chats once per round, votes for B."""
    def __init__(self, session):
        self.session = session
        self.received = []
        self.pid = session.join(self.send)

    async def send(self, msg):
        self.received.append(msg)
        if msg["type"] == "phase" and msg["phase"] == "chat":
            await self.session.handle(self.pid, {"type": "chat", "text": "hello"})
        if msg["type"] == "phase" and msg["phase"] == "vote":
            await self.session.handle(self.pid, {"type": "vote", "target": "B"})


# ---------- winner rule ----------

def test_clear_winner():
    r = decide_winner([{"A": 0, "B": 3, "C": 0}, {"A": 1, "B": 2, "C": 0}])
    assert r == {"winner": "B", "totals": {"A": 1, "B": 5, "C": 0}, "tie_break": None}


def test_tie_broken_by_last_round_votes():
    r = decide_winner([{"A": 2, "B": 1, "C": 0}, {"A": 0, "B": 1, "C": 2}])  # A=2, B=2, C=2 -> last round: C
    assert r["winner"] == "C" and r["tie_break"] == "last_round"


def test_full_tie_is_random():
    r = decide_winner([{"A": 1, "B": 1, "C": 1}])
    assert r["tie_break"] == "random" and r["winner"] in ("A", "B", "C")


# ---------- full run, all 3 conditions ----------

@pytest.mark.parametrize("participants", [
    ["human", "human", "human"],
    ["human", "human", "ai"],
    ["human", "ai", "ai"],
])
def test_full_run(participants):
    async def scenario():
        session = Session(make_cfg(participants), FakeAI())
        bots = [BotHuman(session) for kind in participants if kind == "human"]
        session.maybe_start()
        # vote_seconds is 5: if voting did not end early, 2 rounds would take 10s and this would time out
        await asyncio.wait_for(session.task, timeout=5)
        return session, bots

    session, bots = asyncio.run(scenario())

    assert session.over and session.result["winner"] == "B"
    assert session.round_tallies == [{"A": 0, "B": 3, "C": 0}] * 2   # all 3 players voted for B, both rounds
    assert session.result["totals"]["B"] == 6

    for bot in bots:
        phases = [(m["phase"], m.get("round")) for m in bot.received if m["type"] == "phase"]
        assert phases == [("chat", 1), ("vote", 1), ("feedback", 1), ("chat", 2), ("vote", 2), ("result", None)]
        assert any(m["type"] == "chat" for m in bot.received)

    # blind condition: the server never says who is human or AI
    everything = json.dumps([m for bot in bots for m in bot.received])
    assert '"human"' not in everything and '"ai"' not in everything


def test_ai_players_chat_and_export_has_everything():
    async def scenario():
        session = Session(make_cfg(["human", "ai", "ai"]), FakeAI())
        BotHuman(session)
        session.maybe_start()
        await asyncio.wait_for(session.task, timeout=5)
        return session

    session = asyncio.run(scenario())
    senders = {m["from"] for m in session.messages}
    assert {"B", "C"} <= senders          # both AI players said something
    data = session.export()
    assert set(data) >= {"participants", "messages", "votes", "round_tallies", "result"}


# ---------- how AI players speak ----------

def test_ai_speaking_rules():
    """Each AI writes at most ai_max_messages per round, and nobody writes twice in a row."""
    async def quiet_human(msg):
        pass                                         # a human who never writes or votes

    async def scenario():
        cfg = make_cfg(["human", "ai", "ai"], vote_seconds=0.2)
        cfg.ai_max_messages = 2
        cfg.chat_seconds = 0.6
        cfg.ai_reply_delay = (0.01, 0.02)            # AIs would write ~30 times without the rules
        session = Session(cfg, FakeAI())
        session.join(quiet_human)
        session.maybe_start()
        await asyncio.wait_for(session.task, timeout=5)
        return session

    session = asyncio.run(scenario())
    for r in (1, 2):
        senders = [m["from"] for m in session.messages if m["round"] == r]
        assert senders.count("B") == 2 and senders.count("C") == 2
        assert all(a != b for a, b in zip(senders, senders[1:]))   # no double messages


# ---------- waiting room and edge cases ----------

def test_waits_until_all_humans_are_there():
    async def scenario():
        session = Session(make_cfg(["human", "human", "ai"]), FakeAI())
        BotHuman(session)
        session.maybe_start()
        await asyncio.sleep(0.1)
        return session

    session = asyncio.run(scenario())
    assert session.task is None and session.phase == "waiting"


def test_extra_players_are_rejected():
    async def scenario():
        session = Session(make_cfg(["human", "human", "ai"]), FakeAI())
        BotHuman(session), BotHuman(session)
        third = session.join(lambda m: None)
        session.maybe_start()
        await asyncio.wait_for(session.task, timeout=5)
        late = session.join(lambda m: None)   # after the game
        return third, late

    third, late = asyncio.run(scenario())
    assert third is None and late is None


def test_leaving_the_waiting_room_frees_the_slot():
    session = Session(make_cfg(["human", "human", "ai"]), FakeAI())
    assert session.join(lambda m: None) == "A"
    session.leave("A")
    assert session.join(lambda m: None) == "A"


def test_leaving_during_the_minimum_wait_cancels_the_start():
    async def scenario():
        session = Session(make_cfg(["human", "human", "ai"], min_wait=0.2), FakeAI())
        a, b = BotHuman(session), BotHuman(session)
        session.maybe_start()
        session.leave(b.pid)                 # B leaves while the waiting room timer is running
        await asyncio.sleep(0.4)
        state = (session.task, session.phase, session.over)
        b2 = BotHuman(session)               # a new B arrives: now it should start
        session.maybe_start()
        await asyncio.wait_for(session.task, timeout=5)
        return state, session

    state, session = asyncio.run(scenario())
    assert state == (None, "waiting", False)
    assert session.result is not None


def test_chat_and_votes_outside_their_phase_are_ignored():
    async def scenario():
        session = Session(make_cfg(["human", "ai", "ai"]), FakeAI())
        pid = session.join(lambda m: None)
        await session.handle(pid, {"type": "chat", "text": "too early"})
        await session.handle(pid, {"type": "vote", "target": "A"})
        return session

    session = asyncio.run(scenario())
    assert session.messages == [] and session.round_votes == {}


def test_invalid_vote_target_is_ignored():
    async def scenario():
        session = Session(make_cfg(["human", "ai", "ai"]), FakeAI())
        pid = session.join(lambda m: None)
        session.phase = "vote"
        await session.handle(pid, {"type": "vote", "target": "Z"})
        return session

    assert asyncio.run(scenario()).round_votes == {}


def test_game_stops_when_all_humans_leave():
    async def scenario():
        session = Session(make_cfg(["human", "ai", "ai"]), FakeAI())
        bot = BotHuman(session)
        session.maybe_start()
        await asyncio.sleep(0.05)
        session.leave(bot.pid)
        await asyncio.wait_for(session.task, timeout=5)
        return session

    session = asyncio.run(scenario())
    assert session.over and session.result is None


def test_a_human_who_does_not_vote_counts_as_abstain():
    class Silent(BotHuman):
        async def send(self, msg):          # never votes
            self.received.append(msg)

    async def scenario():
        session = Session(make_cfg(["human", "ai", "ai"], vote_seconds=0.2), FakeAI())
        Silent(session)
        session.maybe_start()
        await asyncio.wait_for(session.task, timeout=5)
        return session

    session = asyncio.run(scenario())
    assert session.round_tallies == [{"A": 0, "B": 2, "C": 0}] * 2  # only the 2 AI votes
