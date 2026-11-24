# Built-in modules
from enum import Enum, auto


class PlayerDir(Enum):
    """Enumerate the directions in which the player can move."""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()
