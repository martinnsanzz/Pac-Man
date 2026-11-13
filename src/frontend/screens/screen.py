# Built-in modules
from abc import ABC, abstractmethod
from enum import Enum, auto

# Installed modules
import pygame

# Local modules
from ..assets import AssetsLoader

Color = tuple[int, int, int]


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

    GAME_OVER = auto()

    CHEATS = auto()

    NONE = auto()


class Screen(ABC):
    """Base screen class for all screens in game.

    Attributes:
        assets: Loader used to get fonts and images.
        screen_w: Width of the arcade surface.
        screen_h: Height of the arcade surface.
        title_font: Font for the big titles (logo).
        button_font: Font for menu options and buttons.
        text_font: Font for regular text.
    """
    TITLE_FONT_SIZE = 100
    BUTTON_FONT_SIZE = 38
    TEXT_FONT_SIZE = 18

    TEXT_COLOR: Color = (150, 150, 150)
    SELECTED_COLOR: Color = (255, 255, 255)

    BOX_PADDING_X = 80
    BOX_PADDING_Y = 10
    BORDER_RADIUS = 15
    BACK_BUTTON_MARGIN = 50

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader) -> None:
        self.assets = assets
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.title_font = assets.get_font("CRACKMAN", self.TITLE_FONT_SIZE)
        self.button_font = assets.get_font("ARCADECLASSIC",
                                           self.BUTTON_FONT_SIZE)
        self.text_font = assets.get_font("BARCADE", self.TEXT_FONT_SIZE)

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

    def draw_title(self, surface: pygame.Surface, text: str,
                   font: pygame.font.Font, color: Color,
                   midtop: tuple[int, int],
                   shadow_color: Color | None = None,
                   shadow_offset: int = 4) -> pygame.Rect:
        """Draw `text` centred on `midtop`, with an optional drop shadow.

        Returns the rect of the title, so the caller can place other
        elements below it.

        Args:
            surface: The pygame surface to be drawn on.
            text: Title text.
            font: Font to render it with.
            color: Text colour.
            midtop: Position of the title's top-centre point.
            shadow_color: Colour of the drop shadow, or None for no shadow.
            shadow_offset: Shadow offset in pixels in x and y.
        """
        title = font.render(text, True, color)
        rect = title.get_rect(midtop=midtop)
        if shadow_color is not None:
            shadow = font.render(text, True, shadow_color)
            surface.blit(shadow, rect.move(shadow_offset, shadow_offset))
        surface.blit(title, rect)
        return rect
