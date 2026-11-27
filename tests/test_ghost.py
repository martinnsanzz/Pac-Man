# Built-in modules
import random

# Installed modules
import pytest

# Local modules
from src.backend import Ghost, Level, PlayerDir
from src.constants import WALL_ALL, WALL_E, WALL_N, WALL_S
from src.parsing import parse_game_config


# Hand-made maze
CORRIDOR = (0, 0)
DEAD_END = (1, 0)
CLOSED = (2, 0)
CROSS = (0, 1)

GRID = [
        [WALL_N | WALL_S, WALL_N | WALL_E | WALL_S, WALL_ALL],
        [0, WALL_ALL, WALL_ALL],
        ]

TRIES = 50


@pytest.fixture
def level() -> Level:
    """Level whose random maze is replaced by the hand-made GRID."""
    lvl = Level(parse_game_config({}), 1)
    lvl.grid = [list(row) for row in GRID]
    return lvl


@pytest.fixture
def ghost() -> Ghost:
    """Ghost with a seeded generator, so every run picks the same way."""
    return Ghost(CROSS, random.Random(0))


class TestOpenDirections:
    """Validation of ``Ghost.open_directions``."""

    def test_corridor(self, ghost: Ghost, level: Level) -> None:
        assert set(ghost.open_directions(level, *CORRIDOR)) == {
                PlayerDir.LEFT, PlayerDir.RIGHT
                }

    def test_intersection(self, ghost: Ghost, level: Level) -> None:
        assert set(ghost.open_directions(level, *CROSS)) == {
                PlayerDir.UP, PlayerDir.DOWN, PlayerDir.LEFT, PlayerDir.RIGHT
                }

    def test_closed(self, ghost: Ghost, level: Level) -> None:
        assert ghost.open_directions(level, *CLOSED) == []

    def test_never_none(self, ghost: Ghost, level: Level) -> None:
        assert PlayerDir.NONE not in ghost.open_directions(level, *CROSS)


class TestChooseDirection:
    """Validation of ``Ghost.choose_direction``."""

    @pytest.mark.parametrize("current", [PlayerDir.UP, PlayerDir.DOWN,
                                         PlayerDir.LEFT, PlayerDir.RIGHT])
    def test_never_turns_back(self, ghost: Ghost, level: Level,
                              current: PlayerDir) -> None:
        for _ in range(TRIES):
            ghost.direction = current
            choice = ghost.choose_direction(level, *CROSS)
            assert choice is not current.opposite

    def test_corridor_keeps_going(self, ghost: Ghost, level: Level) -> None:
        ghost.direction = PlayerDir.RIGHT
        for _ in range(TRIES):
            assert ghost.choose_direction(level, *CORRIDOR) is PlayerDir.RIGHT

    def test_dead_end_turns_back(self, ghost: Ghost, level: Level) -> None:
        assert ghost.choose_direction(level, *DEAD_END) is PlayerDir.LEFT

    def test_closed_cell(self, ghost: Ghost, level: Level) -> None:
        assert ghost.choose_direction(level, *CLOSED) is PlayerDir.NONE

    def test_standing_still_picks_any_exit(self, ghost: Ghost,
                                           level: Level) -> None:
        assert ghost.choose_direction(level, *CORRIDOR) in {
                PlayerDir.LEFT, PlayerDir.RIGHT
                }

    def test_uses_every_exit(self, ghost: Ghost, level: Level) -> None:
        picks = set()
        for _ in range(TRIES):
            ghost.direction = PlayerDir.NONE
            picks.add(ghost.choose_direction(level, *CROSS))
        assert picks == {PlayerDir.UP, PlayerDir.DOWN,
                         PlayerDir.LEFT, PlayerDir.RIGHT}
