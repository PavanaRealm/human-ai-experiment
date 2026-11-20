import pytest

from app.config import DEFAULT_PATH, load_config, parse_config


def test_repo_config_is_valid():
    cfg = load_config()  # the real config.yml in the repo root
    assert len(cfg.participants) == 3


def test_test_config_is_valid():
    cfg = load_config(DEFAULT_PATH.parent / "config.test.yml")  # the short config for manual tests
    assert cfg.participants == ["human", "ai", "ai"] and cfg.chat_seconds == 30


def test_defaults_are_filled_in():
    cfg = parse_config({"participants": ["human", "ai", "ai"]})
    assert cfg.rounds == 2 and cfg.chat_seconds == 60


@pytest.mark.parametrize("bad", [
    ["human", "human"],                # too few
    ["human", "human", "human", "ai"],  # too many
    ["human", "robot", "ai"],          # unknown type
    ["ai", "ai", "ai"],                # no human
    None,                              # missing
])
def test_bad_participants_are_rejected(bad):
    with pytest.raises(ValueError):
        parse_config({"participants": bad})


def test_bad_rounds_are_rejected():
    with pytest.raises(ValueError):
        parse_config({"participants": ["human", "ai", "ai"], "rounds": 0})
