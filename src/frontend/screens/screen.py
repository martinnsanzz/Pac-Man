# Built-in modules
from abc import ABC, abstractmethod
from pathlib import Path

# Installed modules
import pygame

# Local modules
from .action import Action

# ---------- Fonts ----------
ASSETS_PATH = Path(__file__).resolve().parents[3] / "assets"
TITLE_FONT_PATH = ASSETS_PATH / "fonts" / "Crackman.TTF"
SUB_FONT_PATH = ASSETS_PATH / "fonts" / "ARCADECLASSIC.TTF"
TEXT_FONT_PATH = ASSETS_PATH / "fonts" / "ARCADE.TTF"

TITLE_SIZE = 80
SUB_SIZE = 25
TEXT_SIZE = 22

# ---------- UI ----------
TEXT_COLOR = (150, 150, 150)
SELECTED_COLOR = (255, 255, 255)

BOX_PADDING_X = 80
BOX_PADDING_Y = 10
BORDER_RADIUS = 15


class Screen(ABC):
    """Base screen class for all screens in game.

    Attributes:
        title_font: Font to be used in titles across the game.
        sub_font: Font to be used on the options in the main menu.
        text_font: Font to be used in regular text across the game.
    """
    def __init__(self) -> None:
        self.title_font = pygame.font.Font(TITLE_FONT_PATH, TITLE_SIZE)
        self.sub_font = pygame.font.Font(SUB_FONT_PATH, SUB_SIZE)
        self.text_font = pygame.font.Font(TEXT_FONT_PATH, TEXT_SIZE)

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
