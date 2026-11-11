# Installed modules
import pygame

# Local modules
from .assets import AssetsLoader


class HUD():
    PAD = 10

    def __init__(self, assets: AssetsLoader):
        self.assets = assets
        self.hub_icons = self.assets.hud_icons

        self.hud_font = self.assets.get_font("ARCADE", 40)
        self.hud_color = (255, 255, 255)

    def display_hud(self, surface: pygame.Surface, lives: int,
                    score: int, high_score: int,
                    time_left: int) -> None:
        self._display_lives(surface, lives)
        self._display_score(surface, score)
        self._display_high_score(surface, high_score)
        self._display_time_left(surface, time_left)

    def _display_lives(self, surface: pygame.Surface,
                       lives: int) -> None:
        icon = self.hub_icons["LIVE"]
        step = self.assets.SCALED_HUD + self.PAD
        x = self.PAD
        y = surface.get_height() - step

        if lives > 3:
            counter = self.hud_font.render(f"x{lives}", True, self.hud_color)
            surface.blit(counter, (x, y + 5))
            x += counter.get_width() + self.PAD

        for _ in range(min(lives, 3)):
            surface.blit(icon, (x, y))
            x += step


    def _display_score(self, surface: pygame.Surface,
                       score: int) -> None:
        ...

    def _display_high_score(self, surface: pygame.Surface,
                            high_score: int) -> None:
        ...

    def _display_time_left(self, surface: pygame.Surface,
                           time_left: int) -> None:
        ...
