# Installed modules
import pygame

# Local modules
from .action import Action
from .screen import (Screen, SUB_SIZE, TEXT_COLOR, SELECTED_COLOR,
                     BOX_PADDING_X, BOX_PADDING_Y, BORDER_RADIUS)

# --------- UX ----------
UP_KEYS = (pygame.K_UP, pygame.K_w)
DOWN_KEYS = (pygame.K_DOWN, pygame.K_s)

# ---------- UI ----------
TITLE_Y = 0.35

LINE_HEIGHT = SUB_SIZE + 25


class MainMenu(Screen):
    """Main menu screen shown at game start.

    Attributes:
        options: Menu entries as (label, action) pairs, in display order.
        selected: Index of the currently highlighted option.
    """
    def __init__(self) -> None:
        super().__init__()
        self.options: tuple[tuple[str, Action], ...] = (
                ("Start", Action.START_GAME),
                ("Highscores", Action.HIGHSCORES),
                ("Instructions", Action.INSTRUCTIONS),
                ("Exit", Action.QUIT))
        self.selected: int = 0

    def _draw_title(self, surface: pygame.Surface) -> None:
        """Draw the logo of the game on top of the given surface."""
        # TODO: Replace with logo image
        title = self.title_font.render("PAC-MAN", True, (255, 255, 0))
        rect = title.get_rect(center=((surface.get_width() // 2),
                                      (surface.get_height() * TITLE_Y)))
        surface.blit(title, rect)

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

        Arrow or 'W/S' keys move the selection, Enter confirms it.

        Args:
            event: The pygame event to process.

        Returns:
            The action of the selected option when Enter is pressed,
            otherwise Action.PASS.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in UP_KEYS:
                self.navigate(-1)
            elif event.key in DOWN_KEYS:
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
        self._draw_title(surface)
        start_y = surface.get_height() * 0.55
        x = surface.get_width() // 2
        for index, (label, _) in enumerate(self.options):
            color = SELECTED_COLOR if index == self.selected else TEXT_COLOR
            # drawing the text
            text = self.sub_font.render(label, True, color)
            y = start_y + index * LINE_HEIGHT
            rect = text.get_rect(center=(x, y))
            # drawing the box
            box = rect.inflate(BOX_PADDING_X, BOX_PADDING_Y)
            # width=0 fills the box
            # width=2 draws only the outline
            pygame.draw.rect(surface, color, box,
                             width=2, border_radius=BORDER_RADIUS)
            surface.blit(text, rect)
