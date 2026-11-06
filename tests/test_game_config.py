# Installed modules
from typing import Any, Callable
from pathlib import Path
import pytest
import json

# Local modules
from src.parsing import parse_game_config
from src.exceptions import PacManError

VALID_CONFIG: dict[str, Any] = {
    "highscore_filename": "highscore.txt",
    "lives": 3,
    "total_pacgum": 42,
    "pacgum_points": 10,
    "super_pacgum_points": 50,
    "ghost_points": 200,
    "level_time_limit": 90,
    "retro_shader": "on",
}


@pytest.fixture
def valid_config() -> dict[str, Any]:
    """Fresh copy per test, so mutating it never leaks."""
    return dict(VALID_CONFIG)


def test_empty_uses_defaults():
    assert parse_game_config({}).lives == 3


@pytest.mark.parametrize("value", ["yes", "ON", "", True, None, 1])
def test_shader_rejected(valid_config, value):
    valid_config["retro_shader"] = value
    with pytest.raises(PacManError):
        parse_game_config(valid_config)


@pytest.mark.parametrize("value", [0, -1, 11, "abc", 3.5])
def test_lives_rejected(valid_config, value):
    valid_config["lives"] = value
    with pytest.raises(PacManError):
        parse_game_config(valid_config)


def test_bad_extension(valid_config):
    valid_config["highscore_filename"] = "score.csv"
    with pytest.raises(PacManError):
        parse_game_config(valid_config)


def test_valid(valid_config):
    cfg = parse_game_config(valid_config)
    assert cfg.retro_shader is True
