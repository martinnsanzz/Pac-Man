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

        color = self.BORDER_ACTIVE if dev_mode else self.BORDER
        pygame.draw.rect(panel, color, panel.get_rect(),
                         border_radius=self.BORDER_RADIUS,
                         width=self.BORDER_W)

        line_h = self.font.get_linesize() + self.LINE_SPACING
        y = panel.get_height() - self.PADDING
        for entry in reversed(self.dev_log.entries):
            y -= line_h
            if y < self.PADDING:
                break
            text = self.font.render(entry.text, True,
                                    self.COLORS[entry.kind])
            panel.blit(text, (self.PADDING, y))

        surface.blit(panel, rect.topleft)
