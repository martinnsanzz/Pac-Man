# Installed modules
import pygame

# Local modules
from ..assets import AssetsLoader
from ...backend import TileMap
from ...constants import (TILE_SCALE, TILE_PX, WALL_N, WALL_E,
                          WALL_S, WALL_W, MAZE_WIDTH_PX, MAZE_HEIGHT_PX)


class MazeRenderer():
    """Draw a maze grid as tiles, centered on a surface.

    Each cell value in the grid indexes into the tile set and is also read
    as a bitmask of the directions N, E, S and W when drawing wall
    junctions. A border rectangle is drawn around the whole maze. The grid
    is passed on every render call, so the same renderer works for any
    level.

    Attributes:
        assets: Loader providing ``tiles``.
        tiles: Tile surfaces from the assets loader, indexed by cell value.
        wall_px: Wall thickness in pixels, derived from the tile scale.
    """
    WALL_COLOR = (43, 95, 255)

    def __init__(self, assets: AssetsLoader) -> None:
        """Initialize the renderer with the values that don't depend on
        the grid.

        Args:
            assets: Loader providing ``tiles``, ``SCALED_SIZE`` and
                ``SRC_SIZE``.
        """
        self.tiles = assets.tiles
        self.wall_px = 2 * TILE_SCALE

    def render_maze(self, surface: pygame.Surface,
                    grid: list[list[int]]) -> None:
        """Draw the tiles, the outer border and the wall junctions.

        The maze is centered on the surface based on the size of ``grid``.

        Args:
            surface: Surface to draw on.
            grid: 2D list of cell values, indexed as ``grid[row][col]``.
        """
        start_x, start_y = self._maze_origin(surface)

        for row_i, row in enumerate(grid):
            for col_i, val in enumerate(row):
                px, py = TileMap.tile_to_pixel(col_i, row_i)
                surface.blit(self.tiles[val], (start_x + px, start_y + py))

        maze_rect = pygame.Rect(start_x, start_y,
                                MAZE_WIDTH_PX, MAZE_HEIGHT_PX)
        border = maze_rect.inflate(2 * self.wall_px, 2 * self.wall_px)
        pygame.draw.rect(surface, self.WALL_COLOR, border, self.wall_px)

        self._fill_junctions(surface, grid, start_x, start_y)

    def _maze_origin(self, surface: pygame.Surface) -> tuple[int, int]:
        """Top-left of the maze when centered on the surface."""
        return ((surface.get_width() - MAZE_WIDTH_PX) // 2,
                (surface.get_height() - MAZE_HEIGHT_PX) // 2)

    def _fill_junctions(self, surface: pygame.Surface,
                        grid: list[list[int]],
                        start_x: int, start_y: int) -> None:
        """Fill the square where four neighboring cells meet.

        For every interior corner, draw a ``2 * wall_px`` square in
        ``WALL_COLOR`` if at least one of the four adjacent cells has a
        direction bit touching that corner.

        Args:
            surface: Surface to draw on.
            grid: 2D list of cell values, indexed as ``grid[row][col]``.
            start_x: Left pixel coordinate of the maze on the surface.
            start_y: Top pixel coordinate of the maze on the surface.
        """
        wp = self.wall_px
        for r in range(len(grid) - 1):
            for c in range(len(grid[0]) - 1):
                tl, tr = grid[r][c], grid[r][c + 1]
                bl, br = grid[r + 1][c], grid[r + 1][c + 1]
                if (tl & (WALL_E | WALL_S)) or \
                        (tr & (WALL_W | WALL_S)) or \
                        (bl & (WALL_N | WALL_E)) or \
                        (br & (WALL_N | WALL_W)):
                    x = start_x + (c + 1) * TILE_PX
                    y = start_y + (r + 1) * TILE_PX
                    pygame.draw.rect(surface, self.WALL_COLOR,
                                     (x - wp, y - wp, 2 * wp, 2 * wp))
