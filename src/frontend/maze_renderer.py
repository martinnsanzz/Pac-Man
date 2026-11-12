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
    junctions. A border rectangle is drawn around the whole maze.

    Attributes:
        grid: 2D list of cell values, indexed as ``grid[row][col]``.
        tiles: Tile surfaces from the assets loader, indexed by cell value.
        tile_px: Size in pixels of one scaled tile.
        start_x: Left pixel coordinate of the maze on the surface.
        start_y: Top pixel coordinate of the maze on the surface.
        wall_px: Wall thickness in pixels, derived from the tile scale.
        border: Rectangle enclosing the maze, inflated by one wall
            thickness on each side.
    """

    def __init__(self, grid: list[list[int]], assets: AssetsLoader,
                 screen_w: int, screen_h: int) -> None:
        """Initialize the renderer and compute the centered layout.

        Args:
            grid: 2D list of cell values, indexed as ``grid[row][col]``.
            assets: Loader providing ``tiles``, ``SCALED_SIZE`` and
                ``SRC_SIZE``.
            screen_w: Width in pixels of the target surface.
            screen_h: Height in pixels of the target surface.
        """
        self.grid = grid
        self.tiles = assets.tiles
        self.tile_px = assets.SCALED_SIZE

        self.start_x = (screen_w - len(grid[0]) * self.tile_px) // 2
        self.start_y = (screen_h - len(grid) * self.tile_px) // 2
        self.wall_px = 2 * self.tile_px // assets.SRC_SIZE

        maze_rect = pygame.Rect(self.start_x, self.start_y,
                                len(grid[0]) * self.tile_px,
                                len(grid) * self.tile_px)
        self.border = maze_rect.inflate(2 * self.wall_px, 2 * self.wall_px)

    def render_maze(self, surface: pygame.Surface) -> None:
        """Draw the tiles, the outer border and the wall junctions.

        Args:
            surface: Surface to draw on.
        """
        for row_i, row in enumerate(self.grid):
            for col_i, val in enumerate(row):
                surface.blit(self.tiles[val],
                             (self.start_x + col_i * self.tile_px,
                              self.start_y + row_i * self.tile_px))
        pygame.draw.rect(surface, (43, 95, 255), self.border, self.wall_px)
        self._fill_junctions(surface)

    def _fill_junctions(self, surface: pygame.Surface) -> None:
        """Fill the square where four neighboring cells meet.

        For every interior corner, draw a ``2 * wall_px`` square in
        ``WALL_COLOR`` if at least one of the four adjacent cells has a
        direction bit touching that corner.

        Args:
            surface: Surface to draw on.
        """
        wp = self.wall_px
        for r in range(len(self.grid) - 1):
            for c in range(len(self.grid[0]) - 1):
                tl, tr = self.grid[r][c], self.grid[r][c + 1]
                bl, br = self.grid[r + 1][c], self.grid[r + 1][c + 1]
                if (tl & (E | S)) or \
                        (tr & (W | S)) or \
                        (bl & (N | E)) or \
                        (br & (N | W)):
                    x = self.start_x + (c + 1) * self.tile_px
                    y = self.start_y + (r + 1) * self.tile_px
                    pygame.draw.rect(surface, WALL_COLOR,
                                     (x - wp, y - wp, 2 * wp, 2 * wp))
