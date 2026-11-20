"""Load and check config.yml."""
import os
from dataclasses import dataclass
from pathlib import Path

import yaml

PLAYER_IDS = ["A", "B", "C"]

# repo root / config.yml  (backend/app/config.py -> parents[2] is the repo root)
DEFAULT_PATH = Path(__file__).resolve().parents[2] / "config.yml"


@dataclass
class Config:
    participants: list  # e.g. ["human", "human", "ai"]
    rounds: int
    chat_seconds: float
    vote_seconds: float
    feedback_seconds: float
    min_wait_seconds: float
    ai_model: str
    ai_reply_delay: tuple  # (min, max) seconds


def parse_config(raw: dict) -> Config:
    """Turn the raw YAML dict into a Config. Raise ValueError with a clear message if it is wrong."""
    people = raw.get("participants")
    if not (isinstance(people, list) and len(people) == 3 and all(p in ("human", "ai") for p in people)):
        raise ValueError("config: 'participants' must be a list of 3 items, each 'human' or 'ai'")
    if "human" not in people:
        raise ValueError("config: at least one participant must be 'human'")

    rounds = int(raw.get("rounds", 2))
    if rounds < 1:
        raise ValueError("config: 'rounds' must be at least 1")

    ai = raw.get("ai") or {}
    delay = ai.get("reply_delay_seconds", [2, 6])
    if not (isinstance(delay, list) and len(delay) == 2 and 0 <= delay[0] <= delay[1]):
        raise ValueError("config: 'ai.reply_delay_seconds' must be [min, max] with 0 <= min <= max")

    return Config(
        participants=people,
        rounds=rounds,
        chat_seconds=float(raw.get("chat_seconds", 60)),
        vote_seconds=float(raw.get("vote_seconds", 15)),
        feedback_seconds=float(raw.get("feedback_seconds", 8)),
        min_wait_seconds=float(raw.get("min_wait_seconds", 3)),
        ai_model=str(ai.get("model", "")),
        ai_reply_delay=(float(delay[0]), float(delay[1])),
    )


def load_config(path=None) -> Config:
    """Read the YAML file. Path: argument, else env CONFIG_PATH (used in Docker), else repo root."""
    path = Path(path or os.getenv("CONFIG_PATH") or DEFAULT_PATH)
    with open(path) as f:
        return parse_config(yaml.safe_load(f))
