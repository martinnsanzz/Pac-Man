# Built-in modules
from enum import Enum, auto

# Installed modules
import pygame

# Local modules
from ..backend import LogKind, DevLog
from .assets import AssetsLoader
from .screens.screen import Color, RGBA


class LogInput(Enum):
    """What the App must do after the panel handled a key."""
    NONE = auto()
    SUBMIT = auto()
    CLOSE = auto()


class LogPanel:
    """Dev log panel drawn on the left side of the canvas.

    Shows the DevLog entries, newest at the bottom, each colored by its
    kind and the input line while dev mode is open. It also turns key
    presses into edits of the input line; the App decides what submit
    and close do.

    Attributes:
        dev_log: Log whose entries and input text are displayed.
        font: Font used for every line of the panel.
        fade_mask: Cached mask that fades the panel from bottom to top,
            rebuilt when the panel size changes.
    """

    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    # Layout
    FONT_NAME = "CAIROPIXEL"
    FONT_SIZE = 32
    PADDING = 16
    LINE_SPACE = 4

    # Background and border
    BACKGROUND: RGBA = (255, 255, 255, 18)
    BORDER: RGBA = (255, 255, 255, 50)
    BORDER_ACTIVE: RGBA = (255, 255, 255, 160)
    BORDER_W = 2
    BORDER_RADIUS = 12

    # Fade
    DIM_ALPHA = 60
    FADE_START = 0.5
    MIN_ALPHA = 40

    # Input line
    PROMPT = "> "
    CURSOR = "_"
    INPUT_COLOR: Color = (255, 255, 255)
    BLINK_MS = 500

    # Entries
    COLORS: dict[LogKind, Color] = {
        LogKind.INFO: (128, 128, 128),
        LogKind.MESSAGE: (230, 230, 230),
        LogKind.CHEAT: (80, 220, 100),
        LogKind.WARNING: (255, 165, 0),
    }

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def __init__(self, assets: AssetsLoader, dev_log: DevLog) -> None:
        """Keep the log to display and load the panel font.

        Args:
            assets: Loader used to get the panel font.
            dev_log: Log whose entries and input text are displayed.
        """
        self.dev_log = dev_log
        self.font = assets.get_font(self.FONT_NAME, self.FONT_SIZE)
        self.fade_mask: pygame.Surface | None = None

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event) -> LogInput:
        """Type into the input line of the log.

        Backspace deletes and any other key types its character.
        Ctrl+T or Escape asks to close dev mode, Enter asks to submit.

        Args:
            event: The pygame event to process.

        Returns:
            What the App must do next, NONE when the key was handled here.
        """
        if event.type != pygame.KEYDOWN:
            return LogInput.NONE

        ctrl_t = event.mod & pygame.KMOD_CTRL and event.key == pygame.K_t
        if ctrl_t or event.key == pygame.K_ESCAPE:
            return LogInput.CLOSE
        if event.key == pygame.K_RETURN:
            return LogInput.SUBMIT
        if event.key == pygame.K_BACKSPACE:
            self.dev_log.backspace()
        else:
            self.dev_log.add_char(event.unicode)
        return LogInput.NONE

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             dev_mode: bool) -> None:
        """Draw the panel background, entries and input line inside rect.

        Args:
            surface: Surface to draw on (the canvas).
            rect: Area of the surface the panel fills.
            dev_mode: True while the reviewer is typing, highlights the
                border and shows the input line.
        """
        panel = pygame.Surface(rect.size, pygame.SRCALPHA)
        if self.fade_mask is None or self.fade_mask.get_size() != rect.size:
            self.fade_mask = self._build_fade_mask(rect.size)

        pygame.draw.rect(panel, self.BACKGROUND, panel.get_rect(),
                         border_radius=self.BORDER_RADIUS)

        border_color = self.BORDER_ACTIVE if dev_mode else self.BORDER
        pygame.draw.rect(panel, border_color, panel.get_rect(),
                         border_radius=self.BORDER_RADIUS,
                         width=self.BORDER_W)

        line_h = self.font.get_linesize() + self.LINE_SPACE
        if dev_mode:
            y = self._draw_input(panel, line_h)
        else:
            y = panel.get_height() - self.PADDING
        max_w = panel.get_width() - 2 * self.PADDING

        lines: list[tuple[str, Color]] = []
        for entry in self.dev_log.entries:
            for line in self._wrap(entry.text, max_w):
                lines.append((line, self.COLORS[entry.kind]))

        for text, color in reversed(lines):
            y -= line_h
            if y < self.PADDING:
                break
            rendered = self.font.render(text, True, color)
            panel.blit(rendered, (self.PADDING, y))

        if not dev_mode:
            panel.fill((255, 255, 255, self.DIM_ALPHA),
                       special_flags=pygame.BLEND_RGBA_MULT)
        panel.blit(self.fade_mask, (0, 0),
                   special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(panel, rect.topleft)

    # ------------------------------------------------------------------
    # Fade Mask
    # ------------------------------------------------------------------
    def _build_fade_mask(self, size: tuple[int, int]) -> pygame.Surface:
        """Build a white mask whose alpha fades from bottom to top.

        Blended onto the panel with BLEND_RGBA_MULT, it fades the background,
        border and text together, keeping their colors.

        Args:
            size: Width and height of the panel.

        Returns:
            The mask surface, one alpha value per pixel row.
        """
        width, height = size
        mask = pygame.Surface(size, pygame.SRCALPHA)
        for y in range(height):
            pygame.draw.line(mask,
                             (255, 255, 255, self._line_alpha(y, height)),
                             (0, y), (width - 1, y))
        return mask

    def _line_alpha(self, y: int, height: int) -> int:
        """Return the opacity of a line drawn at y inside the panel.

        Lines in the lower part of the panel are fully opaque, above
        FADE_START they fade linearly down to MIN_ALPHA at the top.

        Args:
            y: Top of the line, in panel coordinates.
            height: Height of the panel.

        Returns:
            An alpha between MIN_ALPHA and 255.
        """
        pos = y / height
        limit = 1 - self.FADE_START

        if pos >= limit:
            return 255
        else:
            return int(self.MIN_ALPHA + (255 - self.MIN_ALPHA) * pos / limit)

    # ------------------------------------------------------------------
    # Input Line
    # ------------------------------------------------------------------
    def _draw_input(self, panel: pygame.Surface, line_h: int) -> int:
        """Draw the input line and its separator at the bottom of panel.

        Args:
            panel: Panel surface to draw on, in its own coordinates.
            line_h: Height of one line, spacing included.

        Returns:
            The y above the separator, messages must stay above it.
        """
        if (pygame.time.get_ticks() // self.BLINK_MS) % 2 == 0:
            cursor = self.CURSOR
        else:
            cursor = ""
        y = panel.get_height() - self.PADDING - line_h
        max_w = panel.get_width() - 2 * self.PADDING
        visible = self.dev_log.text
        while self.font.size(self.PROMPT + visible + self.CURSOR)[0] > max_w:
            visible = visible[1:]

        prompt_render = self.font.render(
            self.PROMPT + visible + cursor, True,
            self.INPUT_COLOR)
        panel.blit(prompt_render, (self.PADDING, y))

        pygame.draw.line(panel,
                         self.BORDER,
                         (self.PADDING, y - self.LINE_SPACE),
                         (panel.get_width() - self.PADDING,
                          y - self.LINE_SPACE))
        return y - self.LINE_SPACE

    # ------------------------------------------------------------------
    # Text
    # ------------------------------------------------------------------
    def _wrap(self, text: str, max_w: int) -> list[str]:
        """Split text into lines that fit inside max_w pixels.

        Words are added to the current line until the next one would
        make it wider than max_w, then a new line starts.

        Args:
            text: The message to split.
            max_w: Maximum line width in pixels.

        Returns:
            The lines in reading order, at least one, even for empty text.
        """
        words = text.split(" ")
        current_line = words[0]
        lines: list[str] = []
        for word in words[1:]:
            candidate = current_line + " " + word
            if self.font.size(candidate)[0] <= max_w:
                current_line = candidate
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines
