"""The experiment logic. One Session = one group of 3 players.

Phases:  waiting -> (chat -> vote -> feedback) x rounds -> result
The server runs all timers. Browsers only display what the server sends.
This file knows nothing about WebSockets: a "send" function is all it needs per human.
"""
import asyncio
import logging
import random
import time

from .config import PLAYER_IDS, Config

log = logging.getLogger("session")


def count_votes(votes: dict) -> dict:
    """{"A": "B", "B": "B", "C": "A"} -> {"A": 1, "B": 2, "C": 0}"""
    counts = {p: 0 for p in PLAYER_IDS}
    for target in votes.values():
        counts[target] += 1
    return counts


def decide_winner(round_tallies: list) -> dict:
    """Most votes over all rounds wins. Tie -> most votes in the last round. Still tied -> random."""
    totals = {p: sum(t[p] for t in round_tallies) for p in PLAYER_IDS}
    best = max(totals.values())
    leaders = [p for p in PLAYER_IDS if totals[p] == best]
    if len(leaders) == 1:
        return {"winner": leaders[0], "totals": totals, "tie_break": None}

    last = round_tallies[-1]
    best_last = max(last[p] for p in leaders)
    leaders = [p for p in leaders if last[p] == best_last]
    if len(leaders) == 1:
        return {"winner": leaders[0], "totals": totals, "tie_break": "last_round"}

    return {"winner": random.choice(leaders), "totals": totals, "tie_break": "random"}


class Session:
    def __init__(self, cfg: Config, ai, on_finish=None):
        self.cfg = cfg
        self.ai = ai                    # object with reply() and vote(), see ai_player.py
        self.on_finish = on_finish      # optional async function, called with the saved data (used for MongoDB)
        self.slots = dict(zip(PLAYER_IDS, cfg.participants))  # {"A": "human", "B": "human", "C": "ai"}
        self.connections = {}           # player id -> send function (humans only)
        self.phase = "waiting"
        self.round = 0
        self.messages = []              # full chat log
        self.round_votes = {}           # votes of the current round: voter -> target
        self.votes = []                 # votes of all finished rounds
        self.round_tallies = []         # vote counts per finished round
        self.result = None
        self.over = False               # True when finished or abandoned -> main.py starts a new Session
        self.task = None                # the background task that runs the experiment
        self.all_voted = asyncio.Event()  # set when everyone has voted (ends the vote phase early)

    # ---------- joining and leaving ----------

    def join(self, send):
        """Give a human the first free human slot. Returns "A"/"B"/"C", or None if not possible."""
        if self.phase != "waiting":
            return None
        for pid, kind in self.slots.items():
            if kind == "human" and pid not in self.connections:
                self.connections[pid] = send
                return pid
        return None

    def leave(self, pid):
        self.connections.pop(pid, None)  # in the waiting room this frees the slot
        self._check_all_voted()

    def _all_humans_joined(self):
        return all(pid in self.connections for pid, kind in self.slots.items() if kind == "human")

    def maybe_start(self):
        """Start the experiment when all human slots are filled."""
        if self.task is None and self._all_humans_joined():
            self.task = asyncio.create_task(self.run())  # keep a reference, or the task could be garbage collected

    # ---------- sending ----------

    async def broadcast(self, msg: dict):
        for pid, send in list(self.connections.items()):
            try:
                await send(msg)
            except Exception:  # connection is dead: drop that player, the game goes on
                self.connections.pop(pid, None)

    async def add_message(self, pid, text):
        if self.phase != "chat":  # chat is only allowed in the chat phase
            return
        msg = {"round": self.round, "from": pid, "text": text, "time": time.time()}
        self.messages.append(msg)
        await self.broadcast({"type": "chat", "round": msg["round"], "from": pid, "text": text})

    # ---------- messages from a human ----------

    async def handle(self, pid, msg: dict):
        kind = msg.get("type")
        if kind == "chat":
            text = str(msg.get("text", "")).strip()[:300]
            if text:
                await self.add_message(pid, text)
        elif kind == "vote" and self.phase == "vote":
            if msg.get("target") in PLAYER_IDS:
                self.round_votes[pid] = msg["target"]  # a human may change the vote until time is up
                self._check_all_voted()

    # ---------- the experiment ----------

    async def run(self):
        try:
            await asyncio.sleep(self.cfg.min_wait_seconds)
            if not self._all_humans_joined():  # someone left during the wait: go back to waiting
                self.task = None
                return
            for r in range(1, self.cfg.rounds + 1):
                if not self.connections:  # all humans gone: stop, nobody is watching
                    self.over = True
                    return
                await self._chat_phase(r)
                await self._vote_phase(r)
                if r < self.cfg.rounds:
                    await self._feedback_phase(r)
            await self._finish()
        except Exception:  # without this, an error in a background task would be silent
            log.exception("Session crashed")
            self.over = True

    async def _chat_phase(self, r):
        self.round = r
        self.phase = "chat"
        await self.broadcast({"type": "phase", "phase": "chat", "round": r,
                              "rounds": self.cfg.rounds, "seconds": self.cfg.chat_seconds})
        ai_tasks = [asyncio.create_task(self._ai_chat_loop(pid))
                    for pid, kind in self.slots.items() if kind == "ai"]
        try:
            await asyncio.sleep(self.cfg.chat_seconds)
        finally:
            for t in ai_tasks:
                t.cancel()
            await asyncio.gather(*ai_tasks, return_exceptions=True)

    async def _ai_chat_loop(self, pid):
        """An AI player: wait a random time, maybe say something, repeat. Cancelled when the chat ends."""
        while True:
            await asyncio.sleep(random.uniform(*self.cfg.ai_reply_delay))
            try:
                text = await self.ai.reply(pid, self.messages, self.round)
            except Exception:
                log.exception("AI reply failed")
                continue
            if text:
                await self.add_message(pid, text)

    async def _vote_phase(self, r):
        self.phase = "vote"
        self.round_votes = {}
        self.all_voted.clear()
        await self.broadcast({"type": "phase", "phase": "vote", "round": r,
                              "rounds": self.cfg.rounds, "seconds": self.cfg.vote_seconds})
        try:
            await asyncio.wait_for(self._collect_votes(), self.cfg.vote_seconds)
        except asyncio.TimeoutError:
            pass  # time is up: whoever did not vote is an abstain
        self.votes.append(dict(self.round_votes))
        self.round_tallies.append(count_votes(self.round_votes))

    async def _collect_votes(self):
        ai_ids = [pid for pid, kind in self.slots.items() if kind == "ai"]
        ai_votes = await asyncio.gather(*(self._ai_vote(pid) for pid in ai_ids))
        for pid, vote in zip(ai_ids, ai_votes):
            self.round_votes[pid] = vote
        self._check_all_voted()
        await self.all_voted.wait()

    async def _ai_vote(self, pid):
        try:
            vote = await self.ai.vote(pid, self.messages)
            if vote in PLAYER_IDS:
                return vote
        except Exception:
            log.exception("AI vote failed")
        return random.choice(PLAYER_IDS)  # fallback if the AI call failed

    def _everyone_voted(self):
        voters = [pid for pid, kind in self.slots.items() if kind == "ai" or pid in self.connections]
        return all(pid in self.round_votes for pid in voters)

    def _check_all_voted(self):
        if self.phase == "vote" and self._everyone_voted():
            self.all_voted.set()

    async def _feedback_phase(self, r):
        self.phase = "feedback"
        await self.broadcast({"type": "phase", "phase": "feedback", "round": r,
                              "rounds": self.cfg.rounds, "seconds": self.cfg.feedback_seconds,
                              "tally": self.round_tallies[-1]})  # counts only, not who voted for whom
        await asyncio.sleep(self.cfg.feedback_seconds)

    async def _finish(self):
        self.result = decide_winner(self.round_tallies)
        self.phase = "result"
        self.over = True
        await self.broadcast({"type": "phase", "phase": "result", **self.result,
                              "round_tallies": self.round_tallies})
        if self.on_finish:
            try:
                await self.on_finish(self.export())
            except Exception:  # a database problem must not break the experiment
                log.exception("Saving the session failed")

    def export(self):
        """Everything a researcher needs. This is what gets saved to MongoDB (step e)."""
        return {
            "participants": self.slots,
            "rounds": self.cfg.rounds,
            "messages": self.messages,
            "votes": self.votes,
            "round_tallies": self.round_tallies,
            "result": self.result,
            "finished_at": time.time(),
        }
