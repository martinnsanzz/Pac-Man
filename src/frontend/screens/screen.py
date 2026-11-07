# Built-in modules
from abc import ABC, abstractmethod
from pathlib import Path

# Installed modules
import pygame

# Local modules
from .action import Action

ASSETS_PATH = Path(__file__).resolve().parents[3] / "assets"
FONT_PATH = ASSETS_PATH / "fonts" / "ARCADECLASSIC.TTF"


class Screen(ABC):
    """Base screen class for all screens in game."""
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> Action:
        """Handle a single pygame event for the current screen.

        The keys accepted will be personalized for each screen.

        Args:
            event: The pygame event to process.

        Returns:
            The action of the selected option in the screen.
        """

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the current screen design on the surface.

        Args:
            surface: The pygame surface to be drawn on.
        """
