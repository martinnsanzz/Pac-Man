# Installed modules
from typing import Any
import pytest
import re

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


def _set(cfg, name):
    cfg["highscore_filename"] = name
    return cfg

@pytest.mark.parametrize("name", [
    "highscore.txt",
    "a.txt",                  # 1-char stem
    "HIGH_score-1.txt",
    "score.v2.txt",           # dots in stem
    "a..txt",
    "ünï.txt",                # unicode
    "x" * 200 + ".txt",       # long name
])
def test_filename_valid(valid_config, name):
    cfg = parse_game_config(_set(valid_config, name))
    assert cfg.highscore_filename == name


@pytest.mark.parametrize("name", [
    "", "score", "txt", "score.tx", "score.csv",
    "score.TXT",              # case-sensitive
    "score.txt.bak",
    "score.txt ",             # trailing space after the extension
])
def test_filename_bad_extension(valid_config, name):
    with pytest.raises(PacManError, match=re.escape("must end in '.txt'")):
        parse_game_config(_set(valid_config, name))


def test_filename_empty_stem(valid_config):
    with pytest.raises(PacManError, match="File name empty"):
        parse_game_config(_set(valid_config, ".txt"))


@pytest.mark.parametrize("name", [
    "a/b.txt", "/a.txt", "../a.txt", "dir/.txt",
])
def test_filename_slash(valid_config, name):
    with pytest.raises(PacManError, match=re.escape("invalid char '/'")):
        parse_game_config(_set(valid_config, name))


@pytest.mark.parametrize("name", ["my score.txt", " a.txt", "a .txt"])
def test_filename_space(valid_config, name):
    with pytest.raises(PacManError, match="invalid space"):
        parse_game_config(_set(valid_config, name))


def test_filename_check_order(valid_config):
    # both '/' and space in the stem: your if/elif order decides the message
    with pytest.raises(PacManError, match=re.escape("invalid char '/'")):
        parse_game_config(_set(valid_config, "a b/c.txt"))


@pytest.mark.parametrize("name", [123, None, ["a.txt"], {}, 1.5])
def test_filename_not_a_string(valid_config, name):
    with pytest.raises(PacManError, match="'highscore_filename'"):
        parse_game_config(_set(valid_config, name))


@pytest.fixture
def valid_config() -> dict[str, Any]:
    """Fresh copy per test, so mutating it never leaks."""
    return dict(VALID_CONFIG)


def test_empty_uses_defaults():
    assert parse_game_config({}).lives == 3


@pytest.mark.parametrize("value", ["yes", "ON", "", True, None, 1])
def test_shader_rejected(valid_config, value):
    valid_config["retro_shader"] = value
    with pytest.raises(PacManError, match="Incorrect mode for 'retro_shader'"):
        parse_game_config(valid_config)


@pytest.mark.parametrize("value", [0, -1, 11, "abc", 3.5])
def test_lives_rejected(valid_config, value):
    valid_config["lives"] = value
    with pytest.raises(PacManError):
        parse_game_config(valid_config)


def test_bad_extension(valid_config):
    valid_config["highscore_filename"] = "score.csv"
    with pytest.raises(PacManError, match="Highscore file must be '.txt'"):
        parse_game_config(valid_config)

def test_partial_keeps_other_defaults():
    cfg = parse_game_config({"lives": 5})
    assert cfg.lives == 5 and cfg.total_pacgum == 42


def test_unknown_keys_ignored(valid_config):
    valid_config["foo"] = "bar"
    parse_game_config(valid_config)


def test_valid(valid_config):
    cfg = parse_game_config(valid_config)
    assert cfg.model_dump() == {**VALID_CONFIG, "retro_shader": True}

def test_shader_off(valid_config):
    valid_config["retro_shader"] = "off"
    assert parse_game_config(valid_config).retro_shader is False
