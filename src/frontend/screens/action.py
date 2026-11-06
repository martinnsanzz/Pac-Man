# Built-in modules
from enum import Enum, auto


class Action(Enum):
    """Possible selections from the game menus."""
    START_GAME = auto()
    RESUME = auto()
    BACK = auto()
    QUIT = auto()
    HIGHSCORES = auto()
    INSTRUCTIONS = auto()
    PASS = auto()
