"""Constants shared across backend and frontend."""

# Tiles (maze cells)
TILE_SRC_PX: int = 16
TILE_SCALE: int = 3
TILE_PX: int = TILE_SRC_PX * TILE_SCALE

# Characters (player and ghosts, drawn unscaled)
SPRITE_SRC_PX: int = 16
SPRITE_SCALE: float = 2
SPRITE_PX = SPRITE_SRC_PX * SPRITE_SCALE

# Maze
MAZE_COLS: int = 12
MAZE_ROWS: int = 13
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
