# Installed modules
import pytest

# Local modules
from src.constants import TILE_PX, WALL_ALL 
from src.backend.tilemap import TileMap

GRID = [
    [1, 2, 3],
    [4, 5, 6],
]


class TestTileToPixel:
    def test_origin(self) -> None:
        assert TileMap.tile_to_pixel(0, 0) == (0, 0)

    def test_scales_by_tile_size(self) -> None:
        assert TileMap.tile_to_pixel(3, 2) == (3 * TILE_PX, 2 * TILE_PX)

    def test_col_and_row_are_not_swapped(self) -> None:
        assert TileMap.tile_to_pixel(1, 0) == (TILE_PX, 0)
        assert TileMap.tile_to_pixel(0, 1) == (0, TILE_PX)


class TestTileCenter:
    def test_first_tile_center_is_half_a_tile(self) -> None:
        half = TILE_PX // 2
        assert TileMap.tile_center(0, 0) == (half, half)

    def test_center_is_top_left_plus_half_a_tile(self) -> None:
        x, y = TileMap.tile_to_pixel(3, 2)
        half = TILE_PX // 2
        assert TileMap.tile_center(3, 2) == (x + half, y + half)


class TestPixelToTile:
    @pytest.mark.parametrize("x, y, expected", [
        (0, 0, (0, 0)),
        (TILE_PX - 1, TILE_PX - 1, (0, 0)),     # last pixel of tile 0
        (TILE_PX, TILE_PX, (1, 1)),             # first pixel of tile 1
        (3 * TILE_PX, 2 * TILE_PX, (3, 2)),
        (3 * TILE_PX - 1, 2 * TILE_PX - 1, (2, 1)),
    ])
    def test_boundaries(self, x: int, y: int,
                        expected: tuple[int, int]) -> None:
        assert TileMap.pixel_to_tile(x, y) == expected

    def test_negative_pixels_are_outside_the_maze(self) -> None:
        assert TileMap.pixel_to_tile(-1, -1) == (-1, -1)


class TestRoundTrip:
    @pytest.mark.parametrize("row", range(len(GRID)))
    @pytest.mark.parametrize("col", range(len(GRID[0])))
    def test_top_left_round_trip(self, col: int, row: int) -> None:
        x, y = TileMap.tile_to_pixel(col, row)
        assert TileMap.pixel_to_tile(x, y) == (col, row)

    @pytest.mark.parametrize("row", range(len(GRID)))
    @pytest.mark.parametrize("col", range(len(GRID[0])))
    def test_center_round_trip(self, col: int, row: int) -> None:
        x, y = TileMap.tile_center(col, row)
        assert TileMap.pixel_to_tile(x, y) == (col, row)


class TestGetTile:
    @pytest.mark.parametrize("col, row, expected", [
        (0, 0, 1),    # top-left corner
        (2, 0, 3),    # top-right corner
        (0, 1, 4),    # bottom-left corner
        (2, 1, 6),    # bottom-right corner
        (1, 1, 5),
    ])
    def test_inside_returns_cell_value(self, col: int, row: int,
                                       expected: int) -> None:
        assert TileMap.get_tile(GRID, col, row) == expected

    def test_uses_row_then_col_order(self) -> None:
        # col=2, row=0 must read GRID[0][2], not GRID[2][0] (would crash)
        assert TileMap.get_tile(GRID, 2, 0) == GRID[0][2]

    @pytest.mark.parametrize("col, row", [
        (3, 0),     # one past the last column
        (0, 2),     # one past the last row
        (-1, 0),    # negative column
        (0, -1),    # negative row
        (-1, -1),
        (100, 100),
    ])
    def test_out_of_bounds_is_fully_walled(self, col: int, row: int) -> None:
        assert TileMap.get_tile(GRID, col, row) == WALL_ALL