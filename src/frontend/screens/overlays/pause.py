# Installed modules
import pygame

# Local modules
from .overlay_menu import OverlayMenu
from ..screen import ScreenAction


class Pause(OverlayMenu):
    """Overlay menu shown while the game is paused.

    Offers returning to the main menu, resuming, or quitting. Pressing
    Escape also resumes the game.
    """
    TITLE_TEXT = "PAUSE"
    TITLE_COLOR = (235, 217, 23)
    SHADOW_COLOR = (99, 91, 2)

    OPTIONS = (("Menu", ScreenAction.MAIN_MENU),
               ("Resume", ScreenAction.RESUME),
               ("Quit", ScreenAction.QUIT))

    def handle_event(self, event: pygame.event.Event) -> ScreenAction | None:
        """Resume on Escape, otherwise delegate to the parent menu.

        Args:
            event: The pygame event to process.

        Returns:
            ``ScreenAction.RESUME`` if Escape was pressed, otherwise
            the action returned by the parent overlay menu.
        """
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            return ScreenAction.RESUME
        elif (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) \
            and keys[pygame.K_t]:
            return ScreenAction.DEV_MODE
        return super().handle_event(event)
