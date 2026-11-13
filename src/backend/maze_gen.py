# Installed modules
from mazegen import MazeGenerator


class MazeGen():
    def __init__(self) -> None:
        self.width = 19
        self.height = 20
        self.grid = self.gen_maze()

    def gen_maze(self) -> list[list[int]]:
        generator = MazeGenerator(self.width, self.height,
                                  (0, 0), (1, 1), False)
        generator.generate()
        grid: list[list[int]] = generator.maze
        return grid
