# Installed modules
import pygame

# Local modules
from .paths import SpritesPaths, FontsPaths, TilemapPath


class AssetsLoader():
    """Load all files inside assets/ and converts them to pygame fonts
    or surface

    Attributes:
        tiles: List containing all 16 tiles within the tilemap 16x16 px each
               as a pygame surface.
        sprites: dict containing all sprites for the game as pygame Surfaces.
        fonts: dict containing all fonts for the game as pygame Font.
    """
    SCALE = 2
    TILE_SRC_SIZE = 16
    TILEMAP_COLS = 4
    TILE_PX = TILE_SRC_SIZE * SCALE

    def __init__(self) -> None:
        """Declare the attributes and initialize them to nothing"""
        self.tiles: list[pygame.Surface] = []
        self.sprites: dict[str, pygame.Surface] = {}
        self.fonts: dict[str, pygame.font.Font] = {}

    def load(self) -> None:
        """Loads all assets independently. It modifies class attributes
        directly.
        """
        self._load_tiles()
        self._load_sprites()
        self._load_fonts()

    def _load_tiles(self) -> None:
        """Load the tilemap image and append 16 scaled tiles to `self.tiles`.

        Read the image at `TilemapPath.TILEMAP`, cut it into `self.TILE` x
        `self.TILE` squares laid out row by row in a grid `self.COLS` tiles
        wide, and scale each square to `self.SIZE` x `self.SIZE`. Tiles are
        appended in reading order (left to right, top to bottom).
        """
        tilemap = pygame.image.load(TilemapPath.TILEMAP).convert_alpha()

        for v in range(16):
            rect = pygame.Rect((v % self.TILEMAP_COLS) * self.TILE_SRC_SIZE,
                               (v // self.TILEMAP_COLS) * self.TILE_SRC_SIZE,
                               self.TILE_SRC_SIZE, self.TILE_SRC_SIZE)
            tile = tilemap.subsurface(rect)
            self.tiles.append(pygame.transform.scale(tile,
                                                     (self.TILE_PX,
                                                      self.TILE_PX)))

    def _load_sprites(self) -> None:
        """Load sprites as Surface objects."""
        for key, value in vars(SpritesPaths).items():
            if not key.startswith("__") and not callable(value):
                self.sprites[key] = pygame.image.load(value)

    def _load_fonts(self) -> None:
        """Load fonts as Font objects."""
        for key, value in vars(FontsPaths).items():
            if not key.startswith("__") and not callable(value):
                self.fonts[key] = pygame.font.Font(value[0], value[1])
