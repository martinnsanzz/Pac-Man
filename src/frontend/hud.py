# Installed modules
import pygame

# Local modules
from .assets import AssetsLoader


class HUD():
    def __init__(self, assets: AssetsLoader):
        self.fonts = assets.fonts
        self.sprites = assets.sprites

    def display_hud(self, surface: pygame.Surface, lives: int,
                    score: int, high_score: int,
                    time_left: int) -> None:
        self._display_lives(surface, lives)
        self._display_score(surface, score)
        self._display_high_score(surface, high_score)
        self._display_time_left(surface, time_left)

    def _display_lives(self, surface: pygame.Surface,
                       lives: int) -> None:
        ...

    def _display_score(self, surface: pygame.Surface,
                       score: int) -> None:
        ...

    def _display_high_score(self, surface: pygame.Surface,
                            high_score: int) -> None:
        ...

    def _display_time_left(self, surface: pygame.Surface,
                           time_left: int) -> None:
        ...
