# Installed modules
import pygame

# Local modules
from .screen import Screen, ScreenAction, Color
from .game import Game
from ..assets import AssetsLoader


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
    TITLE_TEXT: str
    TITLE_COLOR: Color
    SHADOW_COLOR: Color
    OPTIONS: tuple[tuple[str, ScreenAction], ...]

    LEFT_KEYS = (pygame.K_LEFT, pygame.K_a)
    RIGHT_KEYS = (pygame.K_RIGHT, pygame.K_d)
    PANEL_SIZE = (500, 250)
    PANEL_COLOR = (20, 20, 40)
    BORDER_COLOR = (43, 95, 255)
    OVERLAY_COLOR = (0, 0, 0, 150)
    BUTTON_SIZE = (140, 50)
    BUTTON_GAP = 20
    TITLE_FONT_SIZE = 70
    TITLE_TOP_PAD = 40
    SHADOW_OFFSET = 4

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader, game: Game) -> None:
        super().__init__(screen_w, screen_h, assets)
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
        """Build one rectangle per option, in a centred row at the bottom."""
        width, _ = self.BUTTON_SIZE
        total = (len(self.OPTIONS) * width
                 + (len(self.OPTIONS) - 1) * self.BUTTON_GAP)
        left = self.panel.centerx - total // 2
        bottom = self.panel.bottom - self.BUTTON_GAP

        buttons = []
        for i in range(len(self.OPTIONS)):
            rect = pygame.Rect((0, 0), self.BUTTON_SIZE)
            rect.bottomleft = (left + i * (width + self.BUTTON_GAP), bottom)
            buttons.append(rect)
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
                        shadow_color=self.SHADOW_COLOR,
                        shadow_offset=self.SHADOW_OFFSET)
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


class Pause(OverlayMenu):
    """Pause menu over the game. Escape resumes."""
    TITLE_TEXT = "PAUSE"
    TITLE_COLOR = (235, 217, 23)
    SHADOW_COLOR = (99, 91, 2)
    OPTIONS = (("Menu", ScreenAction.MAIN_MENU),
               ("Resume", ScreenAction.RESUME),
               ("Quit", ScreenAction.QUIT))

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return ScreenAction.RESUME
        return super().handle_event(event)


class GameOver(OverlayMenu):
    """Game over menu over the game."""
    TITLE_TEXT = "GAME OVER"
    TITLE_COLOR = (255, 40, 40)
    SHADOW_COLOR = (90, 0, 0)
    BUTTON_SIZE = (120, 50)
    OPTIONS = (("Menu", ScreenAction.MAIN_MENU),
               ("Retry", ScreenAction.START_GAME),
               ("Quit", ScreenAction.QUIT))
