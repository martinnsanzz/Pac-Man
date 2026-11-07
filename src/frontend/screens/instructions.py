# Installed modules
import pygame

# Local modules
from .action import Action
from .screen import Screen, FONT_PATH

# ---------- UI ----------
TITLE_SIZE = 25


class Instructions(Screen):
    """Instructions screen with commands and cheat codes."""
    def __init__(self) -> None:
        self.title_font = pygame.font.Font(FONT_PATH, TITLE_SIZE)

    def handle_event(self, event: pygame.event.Event) -> Action:
        """Handle a single pygame event for the Instructions screen.

        Escape to go back.

        Args:
            event: The pygame event to process.

        Returns:
            The action to return or Action.PASS otherwise.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return Action.BACK
        return Action.PASS

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the instructions screen on the surface.

        Args:
            surface: The pygame surface to be drawn on.
        """
        title = self.title_font.render("Instructions:", True, (255, 255, 0))
        rect = title.get_rect(center=(surface.get_width() // 4,
                                      surface.get_height() * 0.15))
        surface.blit(title, rect)
