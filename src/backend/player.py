# Built-in modules
from math import floor

# Local modules
from ..constants import MAZE_COLS, MAZE_ROWS


class Player():
    def __init__(self) -> None:
        self.pos_x = floor(MAZE_COLS / 2)
        self.pos_y = floor(MAZE_ROWS / 2)
        self.speed = 1
