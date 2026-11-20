# src/constants.py
"""Constants shared across backend and frontend."""

from typing import Final

# ── Tiles (maze cells) ─────────────────────────────────────────────
TILE_SRC_PX: Final[int] = 16                       # tile size in the art
TILE_SCALE: Final[int] = 2                         # how much tiles are enlarged
TILE_PX: Final[int] = TILE_SRC_PX * TILE_SCALE     # tile size on screen (32)

# ── Characters (player and ghosts, drawn unscaled) ─────────────────
CHARACTER_SIZE_PX: Final[int] = 16

# ── Maze ───────────────────────────────────────────────────────────
MAZE_COLS: Final[int] = 19
MAZE_ROWS: Final[int] = 20
MAZE_WIDTH_PX: Final[int] = MAZE_COLS * TILE_PX
MAZE_HEIGHT_PX: Final[int] = MAZE_ROWS * TILE_PX

# ── HUD ────────────────────────────────────────────────────────────
HUD_SRC_PX: Final[int] = 16
HUD_SCALE: Final[float] = 2.5
HUD_PX: Final[int] = int(HUD_SRC_PX * HUD_SCALE)   # 40

# Wall bit flags of one maze cell
WALL_N: Final[int] = 1
WALL_E: Final[int] = 2
WALL_S: Final[int] = 4
WALL_W: Final[int] = 8
WALL_ALL: Final[int] = WALL_N | WALL_E | WALL_S | WALL_W  # 15, fully closed

# Sprite sheet layout
TILEMAP_SHEET_COLS: Final[int] = 4
FRUIT_SHEET_COLS: Final[int] = 4
