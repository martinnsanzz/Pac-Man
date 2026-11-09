# Installed modules
import pygame

# Local modules
from .paths import SpritesPaths, FontsPaths


class AssetsLoader():
    def __init__(self) -> None:
        self.tiles: list[pygame.Surface] = []
        self.sprites: dict[str, list[pygame.Surface]] = {}
        self.fonts: dict[str, pygame.font.Font] = {}

    def load(self) -> None:
        self._load_tiles()
        self._load_sprites()
        self._load_fonts()

    def _load_tiles(self) -> None:
        ...

    def _load_sprites(self) -> None:
        ...

    def _load_fonts(self) -> None:
        for key, value in vars(FontsPaths).items():
            if not key.startswith("__") and not callable(value):
                self.fonts[key] = pygame.font.Font(value)