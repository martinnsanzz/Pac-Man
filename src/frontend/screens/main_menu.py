# Installed modules
import pygame

# Local modules
from .screen import Screen, ScreenAction
from ..assets import AssetsLoader


class MainMenu(Screen):
    """Main menu screen shown at game start.

    Attributes:
        options: Menu entries as (label, action) pairs, in display order.
        selected: Index of the currently highlighted option.
    """
    # --------- UX ----------
    UP_KEYS = (pygame.K_UP, pygame.K_w)
    DOWN_KEYS = (pygame.K_DOWN, pygame.K_s)

    # ---------- UI ----------
    TITLE_Y = 0.35

    LINE_HEIGHT = Screen.SUB_SIZE + 40

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader) -> None:
        super().__init__(screen_w, screen_h, assets)
        self.options: tuple[tuple[str, ScreenAction], ...] = (
                ("Start", ScreenAction.START_GAME),
                ("Highscores", ScreenAction.HIGHSCORES),
                ("Instructions", ScreenAction.INSTRUCTIONS),
                ("Exit", ScreenAction.QUIT))
        self.selected: int = 0

    def _draw_title(self, surface: pygame.Surface) -> None:
        """Draw the logo of the game on top of the given surface."""
        # TODO: Replace with logo image
        title = self.title_font.render("PAC-MAN", True, (255, 255, 0))
        rect = title.get_rect(center=((surface.get_width() // 2),
                                      (surface.get_height() * self.TITLE_Y)))
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

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        """Handle a single pygame event for the main menu.

        Arrow or 'W/S' keys move the selection, Enter confirms it.

        Args:
            event: The pygame event to process.

        Returns:
            The action of the selected option when Enter is pressed,
            otherwise Action.PASS.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in self.UP_KEYS:
                self.navigate(-1)
            elif event.key in self.DOWN_KEYS:
                self.navigate(1)
            elif event.key == pygame.K_RETURN:
                _, action = self.options[self.selected]
                return action
            elif event.key == pygame.K_ESCAPE:  # TEMP TO BE DELETED !!!
                return ScreenAction.QUIT
        return ScreenAction.NONE

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the menu screen on the surface.

        Args:
            surface: The pygame surface to be drawn on.
        """
        self._draw_title(surface)
        start_y = surface.get_height() * 0.55
        x = surface.get_width() // 2
        for index, (label, _) in enumerate(self.options):
            color = self.SELECTED_COLOR if index == self.selected \
                else self.TEXT_COLOR
            # drawing the text
            text = self.button_font.render(label, True, color)
            y = start_y + index * self.LINE_HEIGHT
            rect = text.get_rect(center=(x, y))
            # drawing the box
            box = rect.inflate(self.BOX_PADDING_X, self.BOX_PADDING_Y)
            # width=0 fills the box
            # width=2 draws only the outline
            pygame.draw.rect(surface, color, box,
                             width=2, border_radius=self.BORDER_RADIUS)
            surface.blit(text, rect)
