# Built-in modules
from abc import ABC, abstractmethod
from enum import Enum, auto

# Installed modules
import pygame

# Local modules
from ..assets import AssetsLoader


class ScreenAction(Enum):
    """Possible selections from the game menus."""
    QUIT = auto()
    
    START_GAME = auto()
    HIGHSCORES = auto()
    INSTRUCTIONS = auto()

    PAUSE = auto()
    RESUME = auto()
    
    MAIN_MENU = auto()
    BACK = auto()

    RETRY = auto()
    
    CHEATS = auto()
    
    NONE = auto()


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

    BACK_BUTTON_MARGIN = 50

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader) -> None:
        self.assets = assets
        self.title_font = assets.get_font("CRACKMAN", 100)
        self.sub_font = assets.get_font("ARCADECLASSIC", 30)
        self.text_font = assets.get_font("BARCADE", 18)
        self.button_font = assets.get_font("ARCADECLASSIC", 38)
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

    def _draw_back_button(self, surface: pygame.Surface) -> None:
        """Draw a centered "Back" button nead the bottom of the surface.

        Args:
            surface: The pygame surface to be drawn on.
        """
        x = surface.get_width() // 2
        y = surface.get_height() - self.BACK_BUTTON_MARGIN
        text = self.button_font.render("Back", True, self.SELECTED_COLOR)
        rect = text.get_rect(center=(x, y))
        box = rect.inflate(self.BOX_PADDING_X, self.BOX_PADDING_Y)
        pygame.draw.rect(surface, self.SELECTED_COLOR, box,
                         width=2, border_radius=self.BORDER_RADIUS)
        surface.blit(text, rect)
