# Built-in modules
from typing import NamedTuple

# Installed modules
import pygame

# Local modules
from ..screen import Screen, ScreenAction, Color
from ..game import Game
from ...assets import AssetsLoader


class LabelStyle(NamedTuple):
    """Text, font size and color of a label."""
    text: str
    font_size: int
    color: tuple[int, int, int]


class OverlayMenu(Screen):
    """Base for menus drawn as a panel over the frozen game screen.

    Subclasses must define ``TITLE_TEXT``, ``TITLE_COLOR``, ``SHADOW_COLOR``
    and ``OPTIONS``. Each option is a (label, action) pair shown as a
    button in a row at the bottom of the panel.

    Attributes:
        game: Game whose current frame is drawn behind the menu.
        title_font: Font used for the title.
        overlay: Semi-transparent surface covering the whole screen.
        panel: Rectangle of the centred menu panel.
        selected: Index in ``OPTIONS`` of the highlighted button.
        buttons: Button rectangles, in ``OPTIONS`` order, left to right.
    """
    # Defined by subclasses
    TITLE_TEXT: str
    TITLE_COLOR: Color
    TITLE_SHADOW: Color
    OPTIONS: tuple[tuple[str, ScreenAction], ...]

    # Keys
    LEFT_KEYS = (pygame.K_LEFT, pygame.K_a)
    RIGHT_KEYS = (pygame.K_RIGHT, pygame.K_d)

    # Panel
    PANEL_SIZE = (500, 250)
    PANEL_COLOR = (20, 20, 40)
    BORDER_COLOR = (43, 95, 255)
    OVERLAY_COLOR = (0, 0, 0, 150)

    # Title
    TITLE_FONT_SIZE = 70
    TITLE_TOP_PAD = 40
    SHADOW_OFFSET = 4

    # Buttons
    BUTTON_HEIGHT = 50
    BUTTON_MIN_WIDTH = 120
    BUTTON_PAD_X = 20
    BUTTON_GAP = 20

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader, game: Game) -> None:
        super().__init__(assets)
        self.game = game
        self.title_font = assets.get_font("ARCADECLASSIC",
                                          self.TITLE_FONT_SIZE)

        self.overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        self.overlay.fill(self.OVERLAY_COLOR)
        self.panel = pygame.Rect((0, 0), self.PANEL_SIZE)
        self.panel.center = (screen_w // 2, screen_h // 2)

        self.selected = 0
        self.buttons = self._init_buttons()

    def _init_buttons(self) -> list[pygame.Rect]:
        """Build one rectangle per option, sized to its label, in a row."""
        widths = [max(self.BUTTON_MIN_WIDTH,
                      self.button_font.size(label)[0] + 2 * self.BUTTON_PAD_X)
                  for label, _ in self.OPTIONS]
        total = sum(widths) + (len(widths) - 1) * self.BUTTON_GAP
        x = self.panel.centerx - total // 2
        bottom = self.panel.bottom - self.BUTTON_GAP

        buttons = []
        for width in widths:
            rect = pygame.Rect(0, 0, width, self.BUTTON_HEIGHT)
            rect.bottomleft = (x, bottom)
            buttons.append(rect)
            x += width + self.BUTTON_GAP
        return buttons

    def navigate(self, step: int) -> None:
        """Move the selection by ``step``, clamped to the first/last button."""
        self.selected = max(0, min(self.selected + step,
                                   len(self.OPTIONS) - 1))

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        """Left/right move the selection; Enter triggers the selected option.

        Returns:
            The selected option's action on Enter, otherwise ``NONE``.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in self.LEFT_KEYS:
                self.navigate(-1)
            elif event.key in self.RIGHT_KEYS:
                self.navigate(1)
            elif event.key == pygame.K_RETURN:
                return self.OPTIONS[self.selected][1]
        return ScreenAction.NONE

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the game, the dimmed overlay, the panel, title and buttons."""
        self.game.draw(surface)
        surface.blit(self.overlay, (0, 0))
        pygame.draw.rect(surface, self.PANEL_COLOR, self.panel)
        pygame.draw.rect(surface, self.BORDER_COLOR, self.panel, 4)

        self.draw_title(surface, self.TITLE_TEXT, self.title_font,
                        self.TITLE_COLOR,
                        (self.panel.centerx,
                         self.panel.top + self.TITLE_TOP_PAD),
                        shadow_color=self.TITLE_SHADOW,
                        shadow_offset=self.SHADOW_OFFSET)
        self._draw_content(surface)

    def _draw_content(self, surface: pygame.Surface) -> None:
        """Draw what sits below the title. Subclasses can override."""
        self._display_buttons(surface)

    def _display_buttons(self, surface: pygame.Surface) -> None:
        """Draw every button, highlighting the selected one."""
        for i, (label, _) in enumerate(self.OPTIONS):
            rect = self.buttons[i]
            color = (self.SELECTED_COLOR if i == self.selected
                     else self.TEXT_COLOR)
            pygame.draw.rect(surface, color, rect, 3)
            text = self.button_font.render(label, True, color)
            surface.blit(text, text.get_rect(center=rect.center))
