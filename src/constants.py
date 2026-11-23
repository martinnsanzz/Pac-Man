"""Constants shared across backend and frontend."""

# Tiles (maze cells)
TILE_SRC_PX: int = 16
TILE_SCALE: int = 2
TILE_PX: int = TILE_SRC_PX * TILE_SCALE

# Characters (player and ghosts, drawn unscaled)
CHARACTER_SIZE_PX: int = 16

# Maze
MAZE_COLS: int = 19
MAZE_ROWS: int = 20
MAZE_WIDTH_PX: int = MAZE_COLS * TILE_PX
MAZE_HEIGHT_PX: int = MAZE_ROWS * TILE_PX

# HUD
HUD_SRC_PX: int = 16
HUD_SCALE: float = 2.5
HUD_PX: int = int(HUD_SRC_PX * HUD_SCALE)   # 40

# Wall bit flags of one maze cell
WALL_N: int = 1
WALL_E: int = 2
WALL_S: int = 4
WALL_W: int = 8
WALL_ALL: int = WALL_N | WALL_E | WALL_S | WALL_W  # 15, fully closed

# Sprite sheet layout
TILEMAP_SHEET_COLS: int = 4
FRUIT_SHEET_COLS: int = 4

# Arcade screen settings
ARCADE_WIDTH = 672
ARCADE_HEIGHT = 864
