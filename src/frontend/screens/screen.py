# Built-in modules
from abc import ABC, abstractmethod

# Installed modules
import pygame

# Local modules
from .actions import ScreenAction
from ..assets import AssetsLoader


class Screen(ABC):
    """Base screen class for all screens in game.

    Attributes:
        title_font: Font to be used in titles across the game.
        sub_font: Font to be used on the options in the main menu.
        text_font: Font to be used in regular text across the game.
    """
    TITLE_SIZE = 80
    SUB_SIZE = 25
    TEXT_SIZE = 22

    # ---------- UI ----------
    TEXT_COLOR = (150, 150, 150)
    SELECTED_COLOR = (255, 255, 255)

    BOX_PADDING_X = 80
    BOX_PADDING_Y = 10
    BORDER_RADIUS = 15

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader) -> None:
        self.assets = assets
        self.title_font = assets.fonts["CRACKMAN"]
        self.sub_font = assets.fonts["ARCADECLASSIC"]
        self.text_font = assets.fonts["ARCADE"]
        self.screen_w = screen_w
        self.screen_h = screen_h

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        """Handle a single pygame event for the current screen.

        The keys accepted will be personalized for each screen.

        Args:
            event: The pygame event to process.

        Returns:
            The action of the selected option in the screen.
        """

    def update(self, dt: float) -> None:
        """Advance the screen state by dt seconds.

        Does nothing by default; screens with moving parts override it.

        Args:
            dt: Seconds elapsed since the previous frame.
        """

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the current screen design on the surface.

        Args:
            surface: The pygame surface to be drawn on.
        """
