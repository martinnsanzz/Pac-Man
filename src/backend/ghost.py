# Built-in modules
import random

# Local modules
from .level import Level
from .enums import PlayerDir
from .tilemap import TileMap
from ..constants import TILE_PX


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
        target: Center ``(x, y)`` in px of the cell the ghost walks to.
    """
    DEFAULT_SPEED = 4
    OFFSETS: dict[PlayerDir, tuple[int, int]] = {
            PlayerDir.UP: (0, -1),
            PlayerDir.DOWN: (0, 1),
            PlayerDir.LEFT: (-1, 0),
            PlayerDir.RIGHT: (1, 0)}

    def __init__(self, home: tuple[int, int], rng: random.Random,
                 speed: float = DEFAULT_SPEED) -> None:
        """Initialize the ghost at a starting position."""
        self.home = home
        self.rng = rng
        self.speed = speed
        self.direction = PlayerDir.NONE
        x, y = TileMap.tile_center(*home)
        self.pos_x: float = x
        self.pos_y: float = y
        self.target: tuple[float, float] = (self.pos_x, self.pos_y)

    def _pick_next_target(self, level: Level) -> None:
        """Choose a direction at the current center and aim at the next one.

        If no direction is open, the ghost keeps its current target and
        stays still.

        Args:
            level: Level used to look up walls.
        """
        col, row = TileMap.pixel_to_tile(self.pos_x, self.pos_y)
        self.direction = self.choose_direction(level, col, row)
        if self.direction is PlayerDir.NONE:
            return
        dc, dr = self.OFFSETS[self.direction]
        self.target = TileMap.tile_center(col + dc, row + dr)

    def _move(self, distance: float) -> None:
        """Move the ghost along its current direction.

        Args:
            distance: Distance to move, in px.
        """
        match self.direction:
            case PlayerDir.UP:
                self.pos_y -= distance
            case PlayerDir.DOWN:
                self.pos_y += distance
            case PlayerDir.LEFT:
                self.pos_x -= distance
            case PlayerDir.RIGHT:
                self.pos_x += distance

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
        remaining = self.speed * dt * TILE_PX

        while remaining > 0:
            dx = abs(self.target[0] - self.pos_x)
            dy = abs(self.target[1] - self.pos_y)
            distance = dx + dy
            if distance == 0:
                self._pick_next_target(level)
                if self.direction is PlayerDir.NONE:
                    break
                continue

            step = min(remaining, distance)
            self._move(step)
            remaining -= step

            if step == distance:
                self.pos_x, self.pos_y = self.target
