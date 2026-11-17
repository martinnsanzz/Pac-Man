# Installed modules
import pygame

# Local modules
from .assets import AssetsLoader

N, E, S, W = 1, 2, 4, 8
WALL_COLOR = (43, 95, 255)


class MazeRenderer:
    """Draw a maze grid as tiles, centered on a surface.

    Each cell value in the grid indexes into the tile set and is also read
    as a bitmask of the directions N, E, S and W when drawing wall
    junctions. A border rectangle is drawn around the whole maze. The grid
    is passed on every render call, so the same renderer works for any
    level.

    Attributes:
        assets: Loader providing ``tiles``, ``SCALED_SIZE`` and ``SRC_SIZE``.
        screen_w: Width in pixels of the target surface.
        screen_h: Height in pixels of the target surface.
        tiles: Tile surfaces from the assets loader, indexed by cell value.
        tile_px: Size in pixels of one scaled tile.
        wall_px: Wall thickness in pixels, derived from the tile scale.
    """

    def __init__(self, assets: AssetsLoader,
                 screen_w: int, screen_h: int) -> None:
        """Initialize the renderer with the values that don't depend on
        the grid.

        Args:
            assets: Loader providing ``tiles``, ``SCALED_SIZE`` and
                ``SRC_SIZE``.
            screen_w: Width in pixels of the target surface.
            screen_h: Height in pixels of the target surface.
        """
        self.assets = assets
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.tiles = assets.tiles
        self.tile_px = assets.SCALED_SIZE
        self.wall_px = 2 * self.tile_px // assets.SRC_SIZE

    def render_maze(self, surface: pygame.Surface,
                    grid: list[list[int]]) -> None:
        """Draw the tiles, the outer border and the wall junctions.

        The maze is centered on the surface based on the size of ``grid``.

        Args:
            surface: Surface to draw on.
            grid: 2D list of cell values, indexed as ``grid[row][col]``.
        """
        maze_w = len(grid[0]) * self.tile_px
        maze_h = len(grid) * self.tile_px
        start_x = (self.screen_w - maze_w) // 2
        start_y = (self.screen_h - maze_h) // 2

        for row_i, row in enumerate(grid):
            for col_i, val in enumerate(row):
                surface.blit(self.tiles[val],
                             (start_x + col_i * self.tile_px,
                              start_y + row_i * self.tile_px))

        maze_rect = pygame.Rect(start_x, start_y, maze_w, maze_h)
        border = maze_rect.inflate(2 * self.wall_px, 2 * self.wall_px)
        pygame.draw.rect(surface, (43, 95, 255), border, self.wall_px)

        self._fill_junctions(surface, grid, start_x, start_y)

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
                if (tl & (E | S)) or \
                        (tr & (W | S)) or \
                        (bl & (N | E)) or \
                        (br & (N | W)):
                    x = start_x + (c + 1) * self.tile_px
                    y = start_y + (r + 1) * self.tile_px
                    pygame.draw.rect(surface, WALL_COLOR,
                                     (x - wp, y - wp, 2 * wp, 2 * wp))
