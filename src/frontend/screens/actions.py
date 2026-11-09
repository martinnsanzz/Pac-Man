# Built-in modules
from enum import Enum, auto


class ScreenAction(Enum):
    """Possible selections from the game menus."""
    START_GAME = auto()
    RESUME = auto()
    BACK = auto()
    QUIT = auto()
    HIGHSCORES = auto()
    INSTRUCTIONS = auto()
    PAUSE = auto()
    TEXT_BOX = auto()
    NONE = auto()

