# Installed modules
import pygame

# Local modules
from .assets import AssetsLoader


class MazeRenderer:
    """Draws a maze grid as tiles, centered on a surface."""
    def __init__(self, grid: list[list[int]], assets: AssetsLoader,
                 screen_w: int, screen_h: int) -> None:
        self.grid = grid
        self.tiles = assets.tiles
        self.tile_px = assets.SCALED_SIZE
        self.start_x = (screen_w - len(grid[0]) * self.tile_px) // 2
        self.start_y = (screen_h - len(grid) * self.tile_px) // 2

    def render_maze(self, surface: pygame.Surface) -> None:
        for row_i, row in enumerate(self.grid):
            for col_i, val in enumerate(row):
                surface.blit(self.tiles[val],
                             (self.start_x + col_i * self.tile_px,
                              self.start_y + row_i * self.tile_px))
