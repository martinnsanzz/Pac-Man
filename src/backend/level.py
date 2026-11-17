# Installed modules
from mazegen import MazeGenerator

# Local modules
from ..validation import GameConfig


class Level():
    def __init__(self, config: GameConfig, level: int) -> None:
        self.time_left = config.level_time_limit
        self.grid = self.gen_maze(level)

    def decrease_time(self) -> None:
        self.time_left -= 1

    @staticmethod
    def gen_maze(seed: int) -> list[list[int]]:
        generator = MazeGenerator(19, 20,
                                  (0, 0), (1, 1), False,
                                seed)
        generator.generate()
        grid: list[list[int]] = generator.maze
        return grid
