# Built-in modules
import random

# Installed modules
import pytest

# Local modules
from src.backend import Ghost, Level, PlayerDir, TileMap
from src.constants import WALL_ALL, WALL_E, WALL_N, WALL_S, WALL_W
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


# Straight corridor of 4 cells, closed at both ends:
#   (0, 0) only exit RIGHT ... (3, 0) only exit LEFT
LINE = [[WALL_N | WALL_S | WALL_W, WALL_N | WALL_S,
         WALL_N | WALL_S, WALL_N | WALL_S | WALL_E]]


@pytest.fixture
def line_level() -> Level:
    """Level whose maze is the straight LINE corridor."""
    lvl = Level(parse_game_config({}), 1)
    lvl.grid = [list(row) for row in LINE]
    return lvl


@pytest.fixture
def line_ghost() -> Ghost:
    """Ghost standing still at the left end of the LINE corridor."""
    return Ghost((0, 0), random.Random(0))


def tiles(ghost: Ghost, count: float) -> float:
    """Return the seconds the ghost needs to travel `count` tiles."""
    return count / ghost.speed


class TestUpdate:
    """Validation of ``Ghost.update`` movement."""

    def test_one_tile(self, line_ghost: Ghost, line_level: Level) -> None:
        line_ghost.update(tiles(line_ghost, 1), line_level)
        assert (line_ghost.pos_x, line_ghost.pos_y) == \
            TileMap.tile_center(1, 0)
        assert line_ghost.direction is PlayerDir.RIGHT

    def test_half_tile(self, line_ghost: Ghost, line_level: Level) -> None:
        start_x, start_y = TileMap.tile_center(0, 0)
        next_x, _ = TileMap.tile_center(1, 0)
        line_ghost.update(tiles(line_ghost, 0.5), line_level)
        assert line_ghost.pos_x == pytest.approx((start_x + next_x) / 2)
        assert line_ghost.pos_y == start_y

    def test_big_dt_crosses_several_centers(self, line_ghost: Ghost,
                                            line_level: Level) -> None:
        line_ghost.update(tiles(line_ghost, 3), line_level)
        assert (line_ghost.pos_x, line_ghost.pos_y) == \
            TileMap.tile_center(3, 0)

    def test_bounces_at_dead_end(self, line_ghost: Ghost,
                                 line_level: Level) -> None:
        line_ghost.update(tiles(line_ghost, 4), line_level)
        assert (line_ghost.pos_x, line_ghost.pos_y) == \
            TileMap.tile_center(2, 0)
        assert line_ghost.direction is PlayerDir.LEFT

    def test_many_small_steps_stay_on_grid(self, line_ghost: Ghost,
                                           line_level: Level) -> None:
        for _ in range(60):
            line_ghost.update(1 / 60, line_level)
        _, center_y = TileMap.tile_center(0, 0)
        assert line_ghost.pos_y == center_y

    def test_closed_cell_stays_put(self, level: Level) -> None:
        ghost = Ghost(CLOSED, random.Random(0))
        start = (ghost.pos_x, ghost.pos_y)
        ghost.update(1.0, level)
        assert (ghost.pos_x, ghost.pos_y) == start
        assert ghost.direction is PlayerDir.NONE
