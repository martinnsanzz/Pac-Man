# Local modules
from ..constants import TILE_PX, WALL_ALL


class TileMap():
    """Static helpers to convert between pixels and tiles and read cells.

    All pixel positions are relative to the maze origin (its top-left
    corner), not to the screen. A tile is ``TILE_PX`` pixels wide and
    tall, indexed as ``(col, row)``. The class holds no state and is not
    meant to be instantiated.
    """

    # ------------------------------------------------------------------
    # Tile <-> pixel conversion
    # ------------------------------------------------------------------
    @staticmethod
    def tile_to_pixel(col: int, row: int) -> tuple[int, int]:
        """Return the top-left pixel of a tile.

        Args:
            col: Column index of the tile.
            row: Row index of the tile.

        Returns:
            The ``(x, y)`` pixel of the tile's top-left corner, relative to
            the maze origin.
        """
        return col * TILE_PX, row * TILE_PX

    @staticmethod
    def tile_center(col: int, row: int) -> tuple[int, int]:
        """Return the center pixel of a tile.

        Args:
            col: Column index of the tile.
            row: Row index of the tile.

        Returns:
            The ``(x, y)`` pixel at the middle of the tile, relative to the
            maze origin.
        """
        x, y = TileMap.tile_to_pixel(col, row)
        return x + TILE_PX // 2, y + TILE_PX // 2

    @staticmethod
    def pixel_to_tile(x: float, y: float) -> tuple[int, int]:
        """Return the tile that contains a pixel position.

        Args:
            x: Horizontal position in px, relative to the maze origin.
            y: Vertical position in px, relative to the maze origin.

        Returns:
            The ``(col, row)`` index of the tile under ``(x, y)``.
        """
        return int(x // TILE_PX), int(y // TILE_PX)

    # ------------------------------------------------------------------
    # Grid lookup
    # ------------------------------------------------------------------
    @staticmethod
    def get_tile(grid: list[list[int]], col: int,
                 row: int) -> int:
        """Return the cell value at (col, row).

        Positions outside the grid count as fully walled in, so callers
        never need their own bounds checks.

        Args:
            grid: 2D list of cell values, indexed as ``grid[row][col]``.
            col: Column index of the cell.
            row: Row index of the cell.

        Returns:
            The cell value, or ``WALL_ALL`` if ``(col, row)`` is outside
            the grid.
        """
        if col >= len(grid[0]) or col < 0:
            return WALL_ALL
        elif row >= len(grid) or row < 0:
            return WALL_ALL
        return grid[row][col]
