# Installed modules
import pygame

# Local modules
from .paths import SpritesPaths, FontsPaths, TilemapPath, HudPaths


class AssetsLoader():
    """Load all files inside assets/ and converts them to pygame fonts
    or surface

    Attributes:
        tiles: List containing all 16 tiles within the tilemap 16x16 px each
               as a pygame surface.
        sprites: dict containing all sprites for the game as pygame Surfaces.
        fonts: dict containing all fonts for the game as pygame Font.
    """
    SCALE_VAL = 2
    TILEMAP_COLS = 4
    SRC_SIZE = 16
    SCALED_SIZE = SRC_SIZE * SCALE_VAL
    SCALED_HUD = SRC_SIZE * (SCALE_VAL + 0.5)

    def __init__(self) -> None:
        """Declare the attributes and initialize them to nothing"""
        self.fonts: dict[tuple[str, int], pygame.font.Font] = {}
        self.tiles: list[pygame.Surface] = []
        self.sprites: dict[str, pygame.Surface] = {}
        self.hud_icons: dict[str, pygame.Surface] = {}

    def load(self) -> None:
        """Loads all assets independently. It modifies class attributes
        directly.
        """
        self._load_tiles()
        self._load_hud_icons()
        self._load_sprites()

    def _load_tiles(self) -> None:
        """Load the tilemap image and append 16 scaled tiles to `self.tiles`.

        Read the image at `TilemapPath.TILEMAP`, cut it into `self.TILE` x
        `self.TILE` squares laid out row by row in a grid `self.COLS` tiles
        wide, and scale each square to `self.SIZE` x `self.SIZE`. Tiles are
        appended in reading order (left to right, top to bottom).
        """
        tilemap = pygame.image.load(TilemapPath.TILEMAP).convert_alpha()

        for v in range(16):
            rect = pygame.Rect((v % self.TILEMAP_COLS) * self.SRC_SIZE,
                               (v // self.TILEMAP_COLS) * self.SRC_SIZE,
                               self.SRC_SIZE, self.SRC_SIZE)
            tile = tilemap.subsurface(rect)
            self.tiles.append(pygame.transform.scale(tile,
                                                     (self.SCALED_SIZE,
                                                      self.SCALED_SIZE)))
    def _load_hud_icons(self) -> None:
        """Load hud icons as Surface objects."""
        for key, value in vars(HudPaths).items():
            if not key.startswith("__") and not callable(value):
                sprite = pygame.image.load(value)
                scaled = pygame.transform.scale(sprite,
                                                (self.SCALED_HUD,
                                                 self.SCALED_HUD))
                self.hud_icons[key] = scaled
        
    def _load_sprites(self) -> None:
        """Load sprites as Surface objects."""
        for key, value in vars(SpritesPaths).items():
            if not key.startswith("__") and not callable(value):
                sprite = pygame.image.load(value)
                scaled = pygame.transform.scale(sprite,
                                                (self.SCALED_SIZE,
                                                 self.SCALED_SIZE))
                self.sprites[key] = scaled

    def get_font(self, name: str, size: int) -> pygame.font.Font:
        """Return the font `name` at `size`, creating it on first use."""
        key = (name, size)
        if key not in self.fonts:
            self.fonts[key] = pygame.font.Font(getattr(FontsPaths, name), size)
        return self.fonts[key]
