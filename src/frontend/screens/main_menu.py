# Installed modules
import pygame

# Local modules
from .action import Action


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
