# Built-in modules

# Installed modules
import pygame

# Local modules
from .screen import Screen
from .game import Game
from .actions import ScreenAction
from ..assets import AssetsLoader


class Pause(Screen):
    """Display a pause menu on top of the game screen.

    Draw the game, a dimmed overlay and a centred panel with one button per
    entry in ``OPTIONS``.

    Args:
        screen_w: Full screen width.
        screen_h: Full screen height.
        assets: Loader providing the button font.
        game: Game whose current frame is drawn behind the menu.

    Attributes:
        game: Game drawn behind the menu.
        button_font: Font used for the button labels.
        overlay: Semi-transparent surface covering the whole screen.
        panel: Rectangle of the centred menu panel.
        selected: Index in ``OPTIONS`` of the highlighted button.
        buttons: Button rectangles, in ``OPTIONS`` order.
    """
    UP_KEYS = (pygame.K_UP, pygame.K_w)
    DOWN_KEYS = (pygame.K_DOWN, pygame.K_s)
    PANEL_SIZE = (400, 300)

    OPTIONS: tuple[tuple[str, ScreenAction], ...] = (
        ("Menu", ScreenAction.BACK),
        ("Resume", ScreenAction.RESUME),
        ("Quit", ScreenAction.QUIT))
    BUTTON_SIZE = (260, 50)
    BUTTON_GAP = 20

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader, game: Game) -> None:
        super().__init__(int(screen_w / 2), int(screen_h / 3), assets)
        self.game = game
        self.button_font = assets.get_font("ARCADECLASSIC", 38)

        self.overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150))
        self.panel = pygame.Rect((0, 0), self.PANEL_SIZE)
        self.panel.center = (screen_w // 2, screen_h // 2)

        self.selected: int = 0
        self.buttons: list[pygame.Rect] = self._init_buttons()

    def _init_buttons(self) -> list[pygame.Rect]:
        """Build the button rectangles, stacked and centred in the panel.

        Returns:
            One rectangle per entry in ``OPTIONS``, in the same order, top
            to bottom. They share ``panel``'s horizontal centre and are
            spaced ``BUTTON_GAP`` apart.
        """

        buttons = []
        total_height = len(self.OPTIONS) * self.BUTTON_SIZE[1] + \
            (len(self.OPTIONS) - 1) * self.BUTTON_GAP
        top = self.panel.centery - total_height // 2

        for i in range(len(self.OPTIONS)):
            rect = pygame.Rect((0, 0), self.BUTTON_SIZE)
            rect.midtop = (self.panel.centerx,
                           top + i * (self.BUTTON_SIZE[1] + self.BUTTON_GAP))
            buttons.append(rect)
        return buttons

    def navigate(self, step: int) -> None:
        """Move the selection by ``step``, clamped to the valid range.

        The selection does not wrap around: it stops at the first and last
        button.

        Args:
            step: Offset to add to the current position (negative moves up,
                positive moves down).
        """
        self.selected += step
        if self.selected < 0:
            self.selected = 0
        elif self.selected >= len(self.OPTIONS):
            self.selected = len(self.OPTIONS) - 1

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        """Handle a pygame event and return the resulting screen action.

        Up/down keys (``UP_KEYS``, ``DOWN_KEYS``) move the selection. Enter
        triggers the selected option. Escape resumes the game.

        Args:
            event: Event to handle.

        Returns:
            The action of the selected option on Enter,
            ``ScreenAction.RESUME`` on Escape, otherwise
            ``ScreenAction.NONE``.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in self.UP_KEYS:
                self.navigate(-1)
            elif event.key in self.DOWN_KEYS:
                self.navigate(1)
            elif event.key == pygame.K_RETURN:
                _, action = self.OPTIONS[self.selected]
                return action
            elif event.key == pygame.K_ESCAPE:
                return ScreenAction.RESUME
        return ScreenAction.NONE

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the game, the dimmed overlay, the panel and the buttons.

        Args:
            surface: Surface to draw on.
        """
        self.game.draw(surface)
        surface.blit(self.overlay, (0, 0))
        pygame.draw.rect(surface, (20, 20, 40), self.panel)
        pygame.draw.rect(surface, (43, 95, 255), self.panel, 4)

        self.display_buttons(surface)

    def display_buttons(self, surface: pygame.Surface) -> None:
        """Draw every button with its label, highlighting the selected one.

        Args:
            surface: Surface to draw on.
        """
        for i, (label, _) in enumerate(self.OPTIONS):
            rect = self.buttons[i]
            color = self.SELECTED_COLOR if i == self.selected \
                else self.TEXT_COLOR
            pygame.draw.rect(surface, color, rect, 3)
            text = self.button_font.render(label, True, color)
            surface.blit(text, text.get_rect(center=rect.center))
