# Installed modules
from typing import Any
import pytest
import re

# Local modules
from src.parsing import parse_game_config
from src.models import GameConfig
from src.exceptions import PacManError

VALID_CONFIG: dict[str, Any] = {
    "highscores_path": "data/highscores.json",
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


class TestHighscorePath:
    """Validation of ``GameConfig.highscores_path``."""

    @staticmethod
    def parse(cfg: dict[str, Any], path: object) -> GameConfig:
        return parse_game_config({**cfg, "highscores_path": path})

    @pytest.mark.parametrize("path", [
        "data/highscores.json",
        "data/a.json",                    # 1-char stem
        "data/HIGH_score-1.json",
        "data/score.v2.json",             # dots in stem
        "data/a..json",
        "data/ünï.json",                  # unicode
        "data/" + "x" * 200 + ".json",    # long name
        "data/sub/a.json",                # subfolder
        "./data/a.json",                  # leading './'
    ])
    def test_valid(self, valid_config: dict[str, Any], path: str) -> None:
        assert self.parse(valid_config, path).highscores_path == path

    @pytest.mark.parametrize("path, msg", [
        # extension
        ("", "must end in '.json'"),
        ("data/score", "must end in '.json'"),
        ("data/score.jso", "must end in '.json'"),
        ("data/score.JSON", "must end in '.json'"),     # case-sensitive
        ("data/score.json.bak", "must end in '.json'"),
        ("data/score.json ", "must end in '.json'"),    # trailing space
        # empty stem
        (".json", "name is empty"),
        ("data/.json", "name is empty"),
        # space in the file name
        ("data/my score.json", "invalid space"),
        ("data/ a.json", "invalid space"),
        ("data/a .json", "invalid space"),
        # absolute or '..'
        ("/data/a.json", "relative and cannot contain"),
        ("/a.json", "relative and cannot contain"),
        ("../a.json", "relative and cannot contain"),
        ("data/../a.json", "relative and cannot contain"),
        # not inside data/
        ("a.json", "inside 'data/'"),
        ("highscores.json", "inside 'data/'"),
        ("other/a.json", "inside 'data/'"),
        ("database/a.json", "inside 'data/'"),
        ("a/data/b.json", "inside 'data/'"),
    ])
    def test_rejected(self, valid_config: dict[str, Any],
                      path: str, msg: str) -> None:
        with pytest.raises(PacManError, match=re.escape(msg)):
            self.parse(valid_config, path)

    @pytest.mark.parametrize("path", [123, None, ["a.json"], {}, 1.5])
    def test_not_a_string(self, valid_config: dict[str, Any],
                          path: object) -> None:
        with pytest.raises(PacManError, match="'highscores_path'"):
            self.parse(valid_config, path)


class TestConfigLoading:
    """Whole-config behavior: defaults, partial input, unknown keys."""

    def test_valid(self, valid_config: dict[str, Any]) -> None:
        cfg = parse_game_config(valid_config)
        assert cfg.model_dump() == {**VALID_CONFIG, "retro_shader": True}

    def test_empty_uses_defaults(self) -> None:
        cfg = parse_game_config({})
        assert cfg.lives == 3
        assert cfg.highscores_path == "data/highscores.json"

    def test_partial_keeps_other_defaults(self) -> None:
        cfg = parse_game_config({"lives": 5})
        assert cfg.lives == 5
        assert cfg.total_pacgum == 42

    def test_unknown_keys_ignored(self, valid_config: dict[str, Any]) -> None:
        parse_game_config({**valid_config, "foo": "bar"})  # must not raise


class TestRetroShader:

    @pytest.mark.parametrize("raw, expected", [("on", True), ("off", False)])
    def test_accepted(self, valid_config: dict[str, Any],
                      raw: str, expected: bool) -> None:
        cfg = parse_game_config({**valid_config, "retro_shader": raw})
        assert cfg.retro_shader is expected

    @pytest.mark.parametrize("value", ["yes", "ON", "", True, None, 1])
    def test_rejected(self, valid_config: dict[str, Any], value: Any) -> None:
        with pytest.raises(PacManError, match="Incorrect mode"):
            parse_game_config({**valid_config, "retro_shader": value})


class TestLives:

    @pytest.mark.parametrize("value", [1, 10])
    def test_bounds_accepted(self, valid_config: dict[str, Any],
                             value: Any) -> None:
        assert parse_game_config({**valid_config, "lives": value}).lives \
            == value

    @pytest.mark.parametrize("value", [0, -1, 11, "abc", 3.5])
    def test_rejected(self, valid_config: dict[str, Any], value: Any) -> None:
        with pytest.raises(PacManError, match="'lives'"):
            parse_game_config({**valid_config, "lives": value})
