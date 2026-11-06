# Installed modules
import pygame

# Local modules
from .action import Action


# Menu
FONT_SIZE = 64
LINE_HEIGHT = FONT_SIZE + 10
TEXT_COLOR = (150, 150, 150)
SELECTED_COLOR = (255, 255, 255)


class MainMenu:
    """Main menu screen shown at game start.

    Attributes:
        options: Menu entries as (label, action) pairs, in display order.
        selected: Index of the currently highlighted option.
    """
    def __init__(self) -> None:
        self.options: tuple[tuple[str, Action], ...] = (
                ("Start", Action.START_GAME),
                ("Highscores", Action.HIGHSCORES),
                ("Instructions", Action.INSTRUCTIONS),
                ("Exit", Action.QUIT))
        self.selected: int = 0

        # ---------- UI ----------
        self.font = pygame.font.Font(None, FONT_SIZE)

    def navigate(self, step: int) -> None:
        """Move the selection by `step`.

        Args:
            step: Offset to add to the current position (negative moves up,
                positive moves down).
        """
        self.selected += step
        if self.selected < 0:
            self.selected = 0
        elif self.selected >= len(self.options):
            self.selected = len(self.options) - 1

    def handle_event(self, event: pygame.event.Event) -> Action:
        """Handle a single pygame event for the main menu.

        Arrow keys move the selection, Enter confirms it.

        Args:
            event: The pygame event to process.

        Returns:
            The action of the selected option when Enter is pressed,
            otherwise Action.PASS.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.navigate(-1)
            elif event.key == pygame.K_DOWN:
                self.navigate(1)
            elif event.key == pygame.K_RETURN:
                _, action = self.options[self.selected]
                return action
        return Action.PASS

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the menu screen on the surface.

        Args:
            surface: The pygame surface to be drawn on.
        """
        start_y = surface.get_height() * 0.55
        x = surface.get_width() // 2
        for index, (label, _) in enumerate(self.options):
            color = SELECTED_COLOR if index == self.selected else TEXT_COLOR
            text = self.font.render(label, True, color)
            y = start_y + index * LINE_HEIGHT
            rect = text.get_rect(center=(x, y))
            surface.blit(text, rect)
