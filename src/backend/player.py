# Built-in modules
from enum import Enum, auto


class PlayerDir(Enum):
    """Enumerate the directions in which the player can move."""
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
    def __init__(self, start_pos: tuple[float, float],
                 speed: int = 1) -> None:
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
        ...
