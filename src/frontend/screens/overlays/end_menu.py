# Built-in modules
import math

# Installed modules
import pygame
from pydantic import ValidationError

# Local modules
from .overlay_menu import OverlayMenu, LabelStyle
from ..screen import ScreenAction
from ..game import Game
from ...assets import AssetsLoader
from ....validation import HighscoreEntry


class EndMenu(OverlayMenu):
    """Base overlay shown when a game ends, with optional name entry.

    If the score is a highscore, the menu first shows a "NEW HIGHSCORE"
    label and a text input for the player's name. Once the name is
    submitted (or skipped), it falls back to the regular overlay menu
    options.

    Attributes:
        is_highscore: Whether the player still has to be offered name
            entry. Set to False once the entry step is finished.
        entering_name: Whether the name input is currently displayed.
        name: Name typed so far, at most ``MAX_NAME_LEN`` characters.
        shake_start: Tick (ms) when the current shake began, or None
            when the input box is not shaking.
        label_font: Font used for the "ENTER NAME:" label.
        highscore_font: Font used for the "NEW HIGHSCORE !!" label.
        input_font: Font used for the typed name.
    """

    # Name rules
    MAX_NAME_LEN = 10

    # Panel size
    PANEL_SIZE = (550, 250)
    CENTER_OFFSET = 15

    # Fonts size
    SCORE_FONT_SIZE = 40
    INPUT_FONT_SIZE = 32

    # Input box geometry
    INPUT_BOX_WIDTH = 180
    INPUT_BOX_HEIGHT = 35
    INPUT_BORDER_WIDTH = 3
    INPUT_RADIUS = 6

    # Input box colors
    INPUT_BG_COLOR = (0, 0, 0)
    INPUT_BORDER_COLOR = (255, 255, 255)

    # Labels
    INPUT_LABEL = LabelStyle("ENTER NAME:", 32, (255, 255, 255))
    HIGHSCORE_LABEL = LabelStyle("NEW HIGHSCORE !!", 32, (255, 215, 0))
    LABEL_GAP = 8

    # Cursor
    CURSOR_BLINK_MS = 500

    # Score color
    SCORE_COLOR = (255, 215, 0)

    # Shake
    SHAKE_DURATION_MS = 300
    SHAKE_AMPLITUDE_PX = 8
    SHAKE_FREQUENCY = 0.05  # radians per millisecond

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader, game: Game,
                 is_highscore: bool) -> None:
        """Initialize the menu and load its fonts.

        Args:
            screen_w: Screen width in pixels.
            screen_h: Screen height in pixels.
            assets: Loader used to fetch the fonts.
            game: Finished game, used for its score.
            is_highscore: Whether to start in name-entry mode.
        """
        super().__init__(screen_w, screen_h, assets, game)
        self.is_highscore = is_highscore
        self.entering_name = is_highscore
        self.name = ""
        self.shake_start: int | None = None
        self.label_font = assets.get_font(
             "DIGITAL808", self.INPUT_LABEL.font_size)
        self.highscore_font = assets.get_font(
                "DIGITAL808", self.HIGHSCORE_LABEL.font_size)
        self.score_font = assets.get_font(
            "DIGITAL808", self.SCORE_FONT_SIZE)
        self.input_font = assets.get_font("CAIROPIXEL",
                                          self.INPUT_FONT_SIZE)

    def handle_event(self, event: pygame.Event) -> ScreenAction:
        """Process an event, editing the name or delegating to the menu.

        While entering a name, only ``KEYDOWN`` events are handled:
        Backspace deletes the last character, Enter submits, and
        printable ASCII characters are appended up to ``MAX_NAME_LEN``.
        Otherwise the event goes to the parent overlay menu.

        Args:
            event: The pygame event to process.

        Returns:
            ``ScreenAction.NAME_SUBMITTED`` when a valid name is
            submitted, the parent menu's action when not entering a
            name, or None if no screen change is requested.
        """
        if not self.entering_name:
            return super().handle_event(event)
        if event.type != pygame.KEYDOWN:
            return ScreenAction.NONE
        if event.key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]
        elif event.key == pygame.K_RETURN:
            return self._submit()
        elif (
            len(self.name) < self.MAX_NAME_LEN
            and event.unicode
            and event.unicode.isascii()
            and event.unicode.isprintable()
        ):
            self.name += event.unicode
        return ScreenAction.NONE

    def _submit(self) -> ScreenAction:
        """Validate the typed name and leave name-entry mode.

        A non-empty invalid name is cleared and entry continues. An
        empty name ends entry without saving anything.

        Returns:
            ``ScreenAction.NAME_SUBMITTED`` if a valid name was
            entered, otherwise None.
        """
        if self.name and not self._is_valid():
            self.name = ""
            self.shake_start = pygame.time.get_ticks()
            return ScreenAction.NONE
        self.entering_name = False
        self.is_highscore = False
        if self.name:
            return ScreenAction.NAME_SUBMITTED
        return ScreenAction.NONE

    def _is_valid(self) -> bool:
        """Check the name and game score against ``HighscoreEntry``.

        Returns:
            True if a ``HighscoreEntry`` can be built from the current
            name and score, False if validation fails.
        """
        try:
            HighscoreEntry(name=self.name, score=self.game.score)
        except ValidationError:
            return False
        return True

    def _draw_content(self, surface: pygame.Surface) -> None:
        """Draw the name input, or the regular menu once entry is done.

        Args:
            surface: Surface to draw on.
        """
        if self.entering_name:
            self._draw_input(surface)
        else:
            super()._draw_content(surface)

    def _draw_input(self, surface: pygame.Surface) -> None:
        """Draw the name input box with its labels, text and cursor.

        The box sits at the bottom of the panel. Only the box and its
        text shake, the labels stay on the unshaken position.

        Args:
            surface: Surface to draw on.
        """
        base = pygame.Rect(0, 0, self.INPUT_BOX_WIDTH, self.INPUT_BOX_HEIGHT)
        base.midbottom = (self.panel.centerx + self.BUTTON_GAP,
                          self.panel.bottom - self.BUTTON_GAP)
        box = base.move(self._shake_offset(), 0)

        self._draw_labels(surface, base)
        self._draw_box(surface, box)
        self._draw_text(surface, box)

    def _draw_box(self, surface: pygame.Surface, box: pygame.Rect) -> None:
        """Draw the filled input box and its rounded border."""
        pygame.draw.rect(surface, self.INPUT_BG_COLOR, box,
                         border_radius=self.INPUT_RADIUS)
        pygame.draw.rect(surface, self.INPUT_BORDER_COLOR, box,
                         width=self.INPUT_BORDER_WIDTH,
                         border_radius=self.INPUT_RADIUS)

    def _draw_labels(self, surface: pygame.Surface,
                     anchor: pygame.Rect) -> None:
        """Draw the name label left of the anchor, highscore label above."""
        highscore = self.highscore_font.render(
            self.HIGHSCORE_LABEL.text, True, self.HIGHSCORE_LABEL.color)
        surface.blit(highscore, highscore.get_rect(
            center=(self.panel.centerx,
                    self.panel.centery + self.CENTER_OFFSET)))

        self._draw_score(surface, highscore)

        name = self.label_font.render(
            self.INPUT_LABEL.text, True, self.INPUT_LABEL.color)
        surface.blit(name, name.get_rect(
            midright=(anchor.left - self.LABEL_GAP, anchor.centery)))

    def _draw_score(self, surface: pygame.Surface,
                    anchor: pygame.Surface) -> None:
        score = self.score_font.render(
            f"{self.game.score}", True, self.SCORE_COLOR)
        surface.blit(score, score.get_rect(
            center=(self.panel.centerx, self.panel.centery +
                    anchor.get_height() + self.CENTER_OFFSET)
        ))

    def _draw_text(self, surface: pygame.Surface, box: pygame.Rect) -> None:
        """Draw the typed name and the blinking cursor inside the box."""
        text = self.input_font.render(self.name, True, self.TEXT_COLOR)
        text_rect = text.get_rect(center=box.center)
        surface.blit(text, text_rect)

        if pygame.time.get_ticks() // self.CURSOR_BLINK_MS % 2 == 0:
            cursor = pygame.Rect(0, 0, 2, text.get_height() - 6)
            cursor.midleft = (text_rect.right + 2,
                              box.centery)
            pygame.draw.rect(surface, self.TEXT_COLOR, cursor)

    def _shake_offset(self) -> int:
        """Return the current horizontal shake offset in pixels.

        The offset oscillates and fades out over ``SHAKE_DURATION_MS``.
        Resets ``shake_start`` once the shake has finished.

        Returns:
            Horizontal offset in pixels, or 0 when not shaking.
        """
        if self.shake_start is None:
            return 0
        elapsed = pygame.time.get_ticks() - self.shake_start
        if elapsed >= self.SHAKE_DURATION_MS:
            self.shake_start = None
            return 0
        fade = 1 - elapsed / self.SHAKE_DURATION_MS
        return int(self.SHAKE_AMPLITUDE_PX * fade
                   * math.sin(elapsed * self.SHAKE_FREQUENCY))


class GameOver(EndMenu):
    """Overlay menu shown when the player loses.

    Offers returning to the main menu, retrying, or quitting.
    """
    # Title
    TITLE_TEXT = "GAME OVER"
    TITLE_COLOR = (255, 40, 40)
    TITLE_SHADOW = (90, 0, 0)

    # Options
    OPTIONS = (("Menu", ScreenAction.MAIN_MENU),
               ("Retry", ScreenAction.START_GAME),
               ("Quit", ScreenAction.QUIT))


class Win(EndMenu):
    """Overlay menu shown when the player wins.

    Offers returning to the main menu, playing again, or quitting.
    """
    # Title
    TITLE_TEXT = "VICTORY"
    TITLE_COLOR = (60, 255, 110)
    TITLE_SHADOW = (0, 80, 30)

    # Options
    OPTIONS = (("Menu", ScreenAction.MAIN_MENU),
               ("Play again", ScreenAction.START_GAME),
               ("Quit", ScreenAction.QUIT))
