# Installed modules
import pygame

# Local modules
from ..backend import LogKind, DevLog
from .assets import AssetsLoader
from .screens.screen import Color, RGBA


class LogPanel:
    """Dev log panel drawn on the left side of the canvas.

    Shows the DevLog entries, newest at the bottom, each colored by its
    kind and the input line while dev mode is open. The panel only draws.
    Keys are handled by the App.

    Attributes:
        dev_log: Log whose entries and input text are displayed.
        font: Font used for every line of the panel.
    """
    FONT_NAME = "CAIROPIXEL"
    FONT_SIZE = 22
    PADDING = 16
    LINE_SPACING = 4
    BACKGROUND: RGBA = (255, 255, 255, 18)

    BORDER: RGBA = (255, 255, 255, 50)
    BORDER_ACTIVE: RGBA = (255, 255, 255, 160)
    BORDER_W = 2
    BORDER_RADIUS = 12

    COLORS: dict[LogKind, Color] = {
            LogKind.INFO: (128, 128, 128),
            LogKind.MESSAGE: (230, 230, 230),
            LogKind.CHEAT: (80, 220, 100),
            LogKind.WARNING: (255, 165, 0)
            }

    def __init__(self, assets: AssetsLoader, dev_log: DevLog) -> None:
        """Keep the log to display and load the panel font.

        Args:
            assets: Loader used to get the panel font.
            dev_log: Log whose entries and input text are displayed.
        """
        self.dev_log = dev_log
        self.font = assets.get_font(self.FONT_NAME, self.FONT_SIZE)

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
        pygame.draw.rect(panel, self.BACKGROUND, panel.get_rect(),
                         border_radius=self.BORDER_RADIUS)

        border_color = self.BORDER_ACTIVE if dev_mode else self.BORDER
        pygame.draw.rect(panel, border_color, panel.get_rect(),
                         border_radius=self.BORDER_RADIUS,
                         width=self.BORDER_W)

        line_h = self.font.get_linesize() + self.LINE_SPACING
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

        surface.blit(panel, rect.topleft)

    def _wrap(self, text: str, max_w: int) -> list[str]:
        """Split text into lines that fit inside max_w pixels.

        Words are added to the current line until the next one would
        make it wider than max_w, then a new line starts.

        Args:
            text: The message to split.
            max_w: Maximum line width in pixels.

        Returns:
            The lines in reading order, at least on, even for empty text.
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
