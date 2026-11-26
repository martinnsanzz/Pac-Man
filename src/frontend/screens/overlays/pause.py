# Installed modules
import pygame

# Local modules
from src.frontend.assets import AssetsLoader
from src.frontend.screens.game import Game
from .overlay_menu import OverlayMenu, LabelStyle
from ..screen import ScreenAction


class Pause(OverlayMenu):
    """Overlay menu shown while the game is paused.

    Offers returning to the main menu, resuming, or quitting. Pressing
    Escape also resumes the game, and Ctrl + T opens the dev mode.

    Attributes:
        dev_mode_msg_font: Font used for the dev mode hint.
    """

    # Layout
    PANEL_SIZE = (550, 250)
    CENTER_OFFSET = 15

    # Title
    TITLE_TEXT = "PAUSE"
    TITLE_COLOR = (235, 217, 23)
    TITLE_SHADOW = (99, 91, 2)

    # Options
    OPTIONS = (("Menu", ScreenAction.MAIN_MENU),
               ("Resume", ScreenAction.RESUME),
               ("Quit", ScreenAction.QUIT))

    # Hints
    DEV_MODE_LABEL = LabelStyle("Press Ctrl + t for dev mode",
                                32, (107, 114, 117))

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader, game: Game) -> None:
        """Create the pause menu and load the font of the dev mode hint.

        Args:
            screen_w: Width in pixels of the target surface.
            screen_h: Height in pixels of the target surface.
            assets: Loader providing the fonts.
            game: The paused game, drawn behind the menu.
        """
        super().__init__(screen_w, screen_h, assets, game)
        self.dev_mode_msg_font = assets.get_font(
            "CAIROPIXEL", self.DEV_MODE_LABEL.font_size)

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        """Resume on Escape, open dev mode on Ctrl + T, else delegate.

        Args:
            event: The pygame event to process.

        Returns:
            ``ScreenAction.RESUME`` if Escape was pressed,
            ``ScreenAction.DEV_MODE`` if Ctrl + T was pressed, otherwise
            the action returned by the parent overlay menu.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            return ScreenAction.RESUME
        elif (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) \
                and keys[pygame.K_t]:
            return ScreenAction.DEV_MODE
        return super().handle_event(event)

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------
    def _draw_content(self, surface: pygame.Surface) -> None:
        """Draw the dev mode hint, then the regular menu buttons.

        Args:
            surface: Surface to draw on.
        """
        dev_mode_label = self.dev_mode_msg_font.render(
            self.DEV_MODE_LABEL.text, True, self.DEV_MODE_LABEL.color)
        surface.blit(dev_mode_label, dev_mode_label.get_rect(
            center=(self.panel.centerx,
                    self.panel.centery + self.CENTER_OFFSET)))
        return super()._draw_content(surface)
