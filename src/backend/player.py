# Built-in modules
from enum import Enum

# Local modules
from ..constants import TILE_PX


class PlayerDir(Enum):
    """Enumerate the directions in which the player can move."""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Player():
    """Represent the player with a position, direction and speed.

    Attributes:
        pos_x: Horizontal position of the player in px relative to maze.
        pos_y: Vertical position of the player in px relative to maze.
        direction: Current movement direction, or None if the player has
            no direction set.
        speed: Movement speed of the player.
    """
    def __init__(self, start_pos: tuple[float, float],
                 speed: int = 4) -> None:
        """Initialize the player at a starting position.

        Args:
            start_pos: Initial ``(x, y)`` position of the player in px.
            speed: Movement speed of the player. Defaults to 1.
        """
        self.pos_x = start_pos[0]
        self.pos_y = start_pos[1]
        self.direction: PlayerDir | None = None
        self.speed = speed

    def update(self, dt: float) -> None:
        """Update the player state for a time step.

        Args:
            dt: Time elapsed since the previous update in seconds.
        """
        self._move_player(dt)

    def _move_player(self, dt: float) -> None:
        """Move the player in its current direction for one time step."""
        distance = self.speed * TILE_PX * dt

        match self.direction:
            case PlayerDir.UP:
                self.pos_y -= distance
            case PlayerDir.DOWN:
                self.pos_y += distance
            case PlayerDir.LEFT:
                self.pos_x -= distance
            case PlayerDir.RIGHT:
                self.pos_x += distance
