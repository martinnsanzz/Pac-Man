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
    # Keys
    UP_KEYS = (pygame.K_UP, pygame.K_w)
    DOWN_KEYS = (pygame.K_DOWN, pygame.K_s)

    # Title
    TITLE_TEXT = "PAC MAN"
    TITLE_COLOR = (255, 255, 0)
    TITLE_SHADOW = (120, 100, 0)
    TITLE_Y = 0.30            # title height as a fraction of the screen

    # Options
    OPTIONS_Y = 0.55          # first option height, fraction of the screen
    LINE_HEIGHT = Screen.BUTTON_FONT_SIZE + 40
    BUTTON_SIZE = (320, 56)

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def __init__(self, assets: AssetsLoader) -> None:
        """Create the menu with its options and the first one selected.

        Args:
            assets: Loader providing the fonts and sounds.
        """
        super().__init__(assets)
        self.options: tuple[tuple[str, ScreenAction], ...] = (
            ("Start", ScreenAction.START_GAME),
            ("Highscores", ScreenAction.HIGHSCORES),
            ("Instructions", ScreenAction.INSTRUCTIONS),
            ("Exit", ScreenAction.QUIT))
        self.selected: int = 0

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
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

        Arrow or 'W/S' keys move the selection, Enter confirms it. A move
        sound plays only if the selection actually changes.

        Args:
            event: The pygame event to process.

        Returns:
            The action of the selected option when Enter is pressed,
            otherwise ``ScreenAction.NONE``.
        """
        if event.type != pygame.KEYDOWN:
            return ScreenAction.NONE

        if event.key in self.UP_KEYS:
            if self.selected != 0:
                self.assets.play_sound("MENU_MOVE")
            self.navigate(-1)
        elif event.key in self.DOWN_KEYS:
            if self.selected != len(self.options) - 1:
                self.assets.play_sound("MENU_MOVE")
            self.navigate(1)
        elif event.key == pygame.K_RETURN:
            self.assets.play_sound("MENU_SELECT")
            return self.options[self.selected][1]
        return ScreenAction.NONE

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------
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

        Args:
            surface: The pygame surface to be drawn on.
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
