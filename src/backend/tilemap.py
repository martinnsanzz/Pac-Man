# Local modules
from ..constants import TILE_PX, WALL_ALL


class TileMap():
    @staticmethod
    def tile_to_pixel(col: int, row: int) -> tuple[int, int]:
        """Top-left pixel of the tile, relative to the maze origin."""
        return col * TILE_PX, row * TILE_PX

    @staticmethod
    def tile_center(col: int, row: int) -> tuple[int, int]:
        """Center pixel of the tile, relative to the maze origin."""
        x, y = TileMap.tile_to_pixel(col, row)
        return x + TILE_PX // 2, y + TILE_PX // 2

    @staticmethod
    def pixel_to_tile(x: int, y: int) -> tuple[int, int]:
        """Tile index based on the pixel position of the maze"""
        return x // TILE_PX, y // TILE_PX

    @staticmethod
    def get_tile(grid: list[list[int]], col: int,
                 row: int) -> int:
        """Return the cell value at (col, row).

        Positions outside the grid count as fully walled in, so callers
        never need their own bounds checks.
        """
        if col >= len(grid[0]) or col < 0:
            return WALL_ALL
        elif row >= len(grid) or row < 0:
            return WALL_ALL
        return grid[row][col]