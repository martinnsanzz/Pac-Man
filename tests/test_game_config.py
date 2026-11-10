# Installed modules
from typing import Any
import pytest
import re

# Local modules
from src.parsing import parse_game_config
from src.models import GameConfig
from src.exceptions import PacManError

VALID_CONFIG: dict[str, Any] = {
    "highscore_filename": "highscore.json",
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


class TestHighscoreName:
    """Validation of ``GameConfig.highscore_filename``."""

    @staticmethod
    def parse(cfg: dict[str, Any], name: object) -> GameConfig:
        return parse_game_config({**cfg, "highscore_filename": name})

    @pytest.mark.parametrize("name", [
        "highscore.json",
        "a.json",                 # 1-char stem
        "HIGH_score-1.json",
        "score.v2.json",          # dots in stem
        "a..json",
        "ünï.json",               # unicode
        "x" * 200 + ".json",      # long name
    ])
    def test_valid(self, valid_config: dict[str, Any], name: object) -> None:
        assert self.parse(valid_config, name).highscore_filename == name

    @pytest.mark.parametrize("name, msg", [
        # extension
        ("", "must end in '.json'"),
        ("score", "must end in '.json'"),
        ("score.jso", "must end in '.json'"),
        ("score.JSON", "must end in '.json'"),     # case-sensitive
        ("score.json.bak", "must end in '.json'"),
        ("score.json ", "must end in '.json'"),    # trailing space
        # empty stem
        (".json", "File name empty"),
        # slash
        ("a/b.json", "invalid char '/'"),
        ("/a.json", "invalid char '/'"),
        ("../a.json", "invalid char '/'"),
        ("dir/.json", "invalid char '/'"),
        # space
        ("my score.json", "invalid space"),
        (" a.json", "invalid space"),
        ("a .json", "invalid space"),
        # precedence: '/' is checked before space
        ("a b/c.json", "invalid char '/'"),
    ])
    def test_rejected(self, valid_config: dict[str, Any],
                      name: object, msg: str) -> None:
        with pytest.raises(PacManError, match=re.escape(msg)):
            self.parse(valid_config, name)

    @pytest.mark.parametrize("name", [123, None, ["a.json"], {}, 1.5])
    def test_not_a_string(self, valid_config: dict[str, Any],
                          name: object) -> None:
        with pytest.raises(PacManError, match="'highscore_filename'"):
            self.parse(valid_config, name)


class TestConfigLoading:
    """Whole-config behavior: defaults, partial input, unknown keys."""

    def test_valid(self, valid_config: dict[str, Any]) -> None:
        cfg = parse_game_config(valid_config)
        assert cfg.model_dump() == {**VALID_CONFIG, "retro_shader": True}

    def test_empty_uses_defaults(self) -> None:
        assert parse_game_config({}).lives == 3

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
