# Installed modules
import pygame

# Local modules
from .paths import SpritesPaths, FontsPaths, TilemapPath


class AssetsLoader():
    SCALE = 3
    TILE = 16
    COLS = 4
    SIZE = TILE * SCALE

    def __init__(self) -> None:
        self.tiles: list[pygame.Surface] = []
        self.sprites: dict[str, pygame.Surface] = {}
        self.fonts: dict[str, pygame.font.Font] = {}

    def load(self) -> None:
        self._load_tiles()
        self._load_sprites()
        self._load_fonts()

    def _load_tiles(self) -> None:
        tilemap = pygame.image.load(TilemapPath.TILEMAP).convert_alpha()

        for v in range(16):
            rect = pygame.Rect((v % self.COLS) * self.TILE,
                               (v // self.COLS) * self.TILE,
                               self.TILE, self.TILE)
            tile = tilemap.subsurface(rect)
            self.tiles.append(pygame.transform.scale(tile, (self.SIZE, self.SIZE)))

    def _load_sprites(self) -> None:
        for key, value in vars(SpritesPaths).items():
            if not key.startswith("__") and not callable(value):
                self.sprites[key] = pygame.image.load(value)

    def _load_fonts(self) -> None:
        for key, value in vars(FontsPaths).items():
            if not key.startswith("__") and not callable(value):
                self.fonts[key] = pygame.font.Font(value)