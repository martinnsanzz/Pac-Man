# Built-in modules
from enum import IntEnum
from typing import Any, Iterator

# Installed modules
import pygame

# Local modules
from .paths import SpritesPaths, FontsPaths, TilemapPath, HudPaths, SfxPaths


class Fruit(IntEnum):
    """Enumerate the bonus items and their sprite indices.

    Members are integer values starting at 0, so they can be used directly
    as list indices.
    """
    CHERRY = 0
    STRAWBERRY = 1
    ORANGE = 2
    APPLE = 3
    MELON = 4
    SHIP = 5
    BELL = 6
    KEY = 7


def _public_attrs(cls: type) -> Iterator[tuple[str, Any]]:
    """Yield (name, value) for each public, non-callable class attribute."""
    for key, value in vars(cls).items():
        if not key.startswith("__") and not callable(value):
            yield key, value


class AssetsLoader():
    """Load all files inside assets/ and converts them to pygame fonts
    or surface

    Attributes:
        tiles: List containing all 16 tiles within the tilemap 16x16 px each
               as a pygame surface.
        sprites: dict containing all sprites for the game as pygame Surfaces.
        fonts: dict containing all fonts for the game as pygame Font.
    """
    SRC_SIZE = 16
    SCALE_VAL = 2
    HUD_SCALE = 2.5
    SCALED_SIZE = SRC_SIZE * SCALE_VAL
    SCALED_HUD = int(SRC_SIZE * HUD_SCALE)
    TILEMAP_COLS = 4
    FRUIT_COLS = 4

    def __init__(self) -> None:
        """Declare the attributes and initialize them to nothing"""
        self.tiles: list[pygame.Surface] = []
        self.sprites: dict[str, pygame.Surface] = {}
        self.hud_icons: dict[str, pygame.Surface] = {}
        self.fruit_sprites: dict[Fruit, pygame.Surface] = {}
        self.fruit_icons: dict[Fruit, pygame.Surface] = {}
        self.fonts: dict[tuple[str, int], pygame.font.Font] = {}
        self.sounds: dict[str, pygame.mixer.Sound] = {}

    def load(self) -> None:
        """Loads all assets independently. It modifies class attributes
        directly.
        """
        self._load_tiles()
        self._load_sprites()
        self._load_hud_icons()
        self._load_fruits()
        self._load_sounds()

    def _load_tiles(self) -> None:
        """Cut the tilemap into 16 tiles, in reading order."""
        tilemap = pygame.image.load(TilemapPath.TILEMAP).convert_alpha()
        for v in range(16):
            tile = self._cut(tilemap, v, self.TILEMAP_COLS)
            self.tiles.append(self._scale(tile, self.SCALED_SIZE))

    def _load_sprites(self) -> None:
        """Load the in-game sprites (the fruit sheet is handled separately)."""
        for key, path in _public_attrs(SpritesPaths):
            if key == "FRUITS":
                continue
            sprite = pygame.image.load(path).convert_alpha()
            self.sprites[key] = self._scale(sprite, self.SCALED_SIZE)

    def _load_hud_icons(self) -> None:
        """Load one HUD icon per attribute of HudPaths."""
        for key, path in _public_attrs(HudPaths):
            icon = pygame.image.load(path).convert_alpha()
            self.hud_icons[key] = self._scale(icon, self.SCALED_HUD)

    def _load_fruits(self) -> None:
        """Cut the fruit sheet once, scaling each fruit for game and HUD."""
        sheet = pygame.image.load(SpritesPaths.FRUITS).convert_alpha()
        for fruit in Fruit:
            cell = self._cut(sheet, fruit.value, self.FRUIT_COLS)
            self.fruit_sprites[fruit] = self._scale(cell, self.SCALED_SIZE)
            self.fruit_icons[fruit] = self._scale(cell, self.SCALED_HUD)

    def _load_sounds(self) -> None:
        """Load the in-game sound effects."""
        for key, path in _public_attrs(SfxPaths):
            sound = pygame.mixer.Sound(path)
            self.sounds[key] = sound

    def get_font(self, name: str, size: int) -> pygame.font.Font:
        """Return the font `name` at `size`, creating it on first use."""
        key = (name, size)
        if key not in self.fonts:
            self.fonts[key] = pygame.font.Font(getattr(FontsPaths, name), size)
        return self.fonts[key]

    def _cut(self, sheet: pygame.Surface, index: int,
             cols: int) -> pygame.Surface:
        """Return cell `index` of a sheet of SRC_SIZE squares, `cols` wide."""
        rect = pygame.Rect((index % cols) * self.SRC_SIZE,
                           (index // cols) * self.SRC_SIZE,
                           self.SRC_SIZE, self.SRC_SIZE)
        return sheet.subsurface(rect)

    @staticmethod
    def _scale(surface: pygame.Surface, size: int) -> pygame.Surface:
        """Return `surface` scaled to `size` x `size` pixels."""
        return pygame.transform.scale(surface, (size, size))
