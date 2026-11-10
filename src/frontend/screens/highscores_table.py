# Installed modules
import pygame

# Local modules
from .actions import ScreenAction
from .screen import Screen
from ..assets import AssetsLoader
from ...backend import Highscores


class HighscoresTable(Screen):
    """Highscores screen with sorted entries.

    Args:
        highscores: The table of entries to display.
    """
    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader, highscores: Highscores) -> None:
        super().__init__(screen_w, screen_h, assets)
        self.highscores = highscores

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        """Handle a single pygame event for the Highscores screen.

        Enter to go back or Escape to quit the game.

        Args:
            event: The pygame event to process.

        Returns:
            The action to return or Action.NONE otherwise.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return ScreenAction.BACK
        return ScreenAction.NONE

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the Highscores screen on the surface.

        Args:
            surface: The pygame surface to be drawn on.
        """
