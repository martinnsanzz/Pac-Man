# Installed modules
import pygame

# Local modules
from .screen import Screen, ScreenAction
from .game import Game
from ..assets import AssetsLoader


class GameOver(Screen):
    """Display a game over menu on top of the game screen.

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
        ("Menu", ScreenAction.MAIN_MENU),
        ("Retry", ScreenAction.RESTART),
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