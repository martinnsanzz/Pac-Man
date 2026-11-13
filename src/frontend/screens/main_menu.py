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
    UP_KEYS = (pygame.K_UP, pygame.K_w)
    DOWN_KEYS = (pygame.K_DOWN, pygame.K_s)

    TITLE_TEXT = "PAC MAN"
    TITLE_COLOR = (255, 255, 0)
    TITLE_Y = 0.30
    OPTIONS_Y = 0.55
    LINE_HEIGHT = Screen.BUTTON_FONT_SIZE + 40

    TITLE_SHADOW = (120, 100, 0)
    BUTTON_SIZE = (320, 56)
    DARK_TEXT = (12, 14, 16)

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader) -> None:
        super().__init__(screen_w, screen_h, assets)
        self.options: tuple[tuple[str, ScreenAction], ...] = (
            ("Start", ScreenAction.START_GAME),
            ("Highscores", ScreenAction.HIGHSCORES),
            ("Instructions", ScreenAction.INSTRUCTIONS),
            ("Exit", ScreenAction.QUIT))
        self.selected: int = 0

    def navigate(self, step: int) -> None:
        """Move the selection by `step`, clamped to the first/last option.

        Args:
            step: Offset to add to the current position (negative moves up,
                positive moves down).
        """
        self.selected = max(0, min(self.selected + step,
                                   len(self.options) - 1))

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
                return self.options[self.selected][1]
        return ScreenAction.NONE

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the title and the menu options on the surface.

        Args:
            surface: The pygame surface to be drawn on.
        """
        width, height = surface.get_size()
        self.draw_title(surface, self.TITLE_TEXT, self.title_font,
                        self.TITLE_COLOR,
                        (width // 2, int(height * self.TITLE_Y)),
                        shadow_color=self.TITLE_SHADOW)
        self._draw_options(surface)

    def _draw_options(self, surface: pygame.Surface) -> None:
        """Draw every option as an outlined button, highlighting the
        selected one.
        """
        width, height = surface.get_size()
        start_y = int(height * self.OPTIONS_Y)

        for index, (label, _) in enumerate(self.options):
            selected = index == self.selected
            color = self.SELECTED_COLOR if selected else self.TEXT_COLOR

            box = pygame.Rect((0, 0), self.BUTTON_SIZE)
            box.center = (width // 2, start_y + index * self.LINE_HEIGHT)

            pygame.draw.rect(surface, color, box, width=2,
                             border_radius=self.BORDER_RADIUS)
            text = self.button_font.render(label, True, color)
            surface.blit(text, text.get_rect(center=box.center))
