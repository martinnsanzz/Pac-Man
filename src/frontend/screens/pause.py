# Built-in modules

# Installed modules
import pygame
from mazegen import MazeGenerator

# Local modules
from .screen import Screen
from .actions import ScreenAction
from ..assets import AssetsLoader


class Pause(Screen):
    """Pause screen that will pop-up on top of the game screen."""
    # --------- UX ----------
    LEFT_KEYS = (pygame.K_LEFT, pygame.K_a)
    RIGHT_KEYS = (pygame.K_RIGHT, pygame.K_d)

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader) -> None:
        super().__init__(int(screen_w / 2), int(screen_h / 3), assets)

        self.options: tuple[tuple[str, ScreenAction], ...] = (
        ("Menu", ScreenAction.BACK),
        ("Resume", ScreenAction.RESUME),
        ("Quit", ScreenAction.QUIT))

        self.selected: int = 0

    def navigate(self, step: int) -> None:
        """Move the selection by `step`.

        Args:
            step: Offset to add to the current position (negative moves up,
                positive moves down).
        """
        self.selected += step
        if self.selected < 0:
            self.selected = 0
        elif self.selected >= len(self.options):
            self.selected = len(self.options) - 1

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        if event.type == pygame.KEYDOWN:
            if event.key in self.LEFT_KEYS:
                self.navigate(-1)
            elif event.key in self.RIGHT_KEYS:
                self.navigate(1)
            elif event.key == pygame.K_RETURN:
                _, action = self.options[self.selected]
                return action
        return ScreenAction.NONE

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (0, 255, 0), (30, 0, 40, 60))