# Built-in modules
import random

# Local modules
from .level import Level
from .enums import PlayerDir
from .tilemap import TileMap


class Ghost:
    """A ghost that roams the maze on its own.

    Moves from tile center to tile center. At each center it picks a new
    direction, so it never stops and never walks into a wall.

    Attributes:
        home: Corner cell ``(col, row)`` where the ghost spawns.
        rng: Random generator for direction choices, injected so
            tests are repeatable.
        speed: Movement speed in tiles per second.

        direction: Current movement direction.
        pos_x: Horizontal position in px, relative to the maze.
        pos_y: Vertical position in px, relative to the maze.
    """
    DEFAULT_SPEED = 4

    def __init__(self, home: tuple[int, int], rng: random.Random,
                 speed: float = DEFAULT_SPEED) -> None:
        """Initialize the ghost at a starting position."""
        self.home = home
        self.rng = rng
        self.speed = speed
        self.direction = PlayerDir.NONE
        self.pos_x, self.pos_y = TileMap.tile_center(*home)

    def open_directions(self, level: Level,
                        col: int, row: int) -> list[PlayerDir]:
        """Return the directions without a wall from a cell.

        Args:
            level: Level used to look up walls.
            col: Column of the cell.
            row: Row of the cell.

        Returns:
            Every direction the ghost could move in, never NONE.
        """
        open_directions: list[PlayerDir] = []
        for direction in PlayerDir:
            if direction == PlayerDir.NONE:
                continue
            if not level.has_wall(col, row, direction):
                open_directions.append(direction)
        return open_directions

    def choose_direction(self, level: Level,
                         col: int, row: int) -> PlayerDir:
        """Pick the direction to take from a tile center.

        Picks randomly among the open directions, excluding the way back
        unless it is the only exit (a dead end).

        Args:
            level: Level used to look up walls.
            col: Column of the cell.
            row: Row of the cell.

        Returns:
            The chosen direction.
        """
        candidates = self.open_directions(level, col, row)
        if not candidates:
            return PlayerDir.NONE
        back = self.direction.opposite
        if len(candidates) > 1 and back in candidates:
            candidates.remove(back)
        return self.rng.choice(candidates)

    def update(self, dt: float, level: Level) -> None:
        """Move the ghost for a time step.

        Travels ``speed * dt`` tiles, choosing a new direction at every tile
        center it reaches.

        Args:
            dt: Time elapsed since the previous update, in seconds.
            level: Level used to look up walls.
        """
