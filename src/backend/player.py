# Built-in modules
from enum import Enum, auto

# Local modules
from ..constants import TILE_PX


class PlayerDir(Enum):
    """Enumerate the directions in which the player can move."""
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Player():
    """Represent the player with a position, direction and speed.

    Attributes:
        pos_x: Horizontal position of the player in px relative to maze.
        pos_y: Vertical position of the player in px relative to maze.
        direction: Current movement direction, or None if the player has
            no direction set.
        speed: Movement speed of the player.
    """
    def __init__(self, start_pos: tuple[int, int],
                 speed: int = 4) -> None:
        """Initialize the player at a starting position.

        Args:
            start_pos: Initial ``(x, y)`` position of the player in px.
            speed: Movement speed of the player. Defaults to 1.
        """
        print(start_pos)
        self.pos_x = start_pos[0]
        self.pos_y = start_pos[1]
        self.direction: PlayerDir = PlayerDir.NONE
        self.speed = speed

    def update(self, dt: float) -> None:
        """Update the player state for a time step.

        Args:
            dt: Time elapsed since the previous update in seconds.
        """
        self._move_player(dt)

    def _move_player(self, dt: float) -> None:
        """Move the player in its current direction for one time step."""
        distance = int(self.speed * TILE_PX * dt)

        match self.direction:
            case PlayerDir.UP:
                self.pos_y -= distance
            case PlayerDir.DOWN:
                self.pos_y += distance
            case PlayerDir.LEFT:
                self.pos_x -= distance
            case PlayerDir.RIGHT:
                self.pos_x += distance

    def has_reached(self, point: tuple[float, float]) -> bool:
        """Return True once the player has reached or passed point
        along its direction of travel."""
        x, y = point

        match self.direction:
            case PlayerDir.UP:
                return self.pos_y <= y
            case PlayerDir.DOWN:
                return self.pos_y >= y
            case PlayerDir.LEFT:
                return self.pos_x <= x
            case PlayerDir.RIGHT:
                return self.pos_x >= x
            case _:
                return False

    def center_pos_to_cell(self, center_pos: tuple[int, int]) -> None:
        """Center position of player to cell center"""
        self.pos_x = center_pos[0]
        self.pos_y = center_pos[1]
