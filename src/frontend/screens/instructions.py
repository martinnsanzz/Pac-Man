# Installed modules
import pygame

# Local modules
from .screen import Screen, ScreenAction
from ..assets import AssetsLoader

# TODO: read values of pacgums from config

Row = tuple[pygame.Surface, pygame.Surface]


class Instructions(Screen):
    """Instructions screen with controls, rules and cheat codes.

    Attributes:
        sub_title_font: Font used for the title and the section headers.
        sections: Pre-rendered (header, rows) pairs, each row being a
            (key, description) pair of surfaces.
    """
    TITLE_TEXT = "INSTRUCTIONS"
    TITLE_Y_RATIO = 0.12
    TITLE_GAP = 50
    SUB_TITLE_SIZE = 50
    LINE_HEIGHT = 32
    SECTION_GAP = 24
    MARGIN_RATIO = 0.125
    DESC_X_RATIO = 0.45
    INDENT = 24

    HEADER_COLOR = (255, 255, 0)
    SHADOW_COLOR = (99, 91, 2)
    KEY_COLOR = (0, 255, 255)

    CONTENT: dict[str, tuple[tuple[str, str], ...]] = {
        "CONTROLS": (("ARROWS / WASD", "Move Pac-Man"),
                     ("ESC", "Pause / resume"),
                     ("ENTER", "Select / go back")),
        "RULES": (("PAC-GUM", "Gives points"),
                  ("SUPER PAC-GUM", "Gives points and lets you eat ghosts")),
        "CHEAT CODES": (("TODO", "Coming soon"),),
    }

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader) -> None:
        super().__init__(screen_w, screen_h, assets)
        self.sub_title_font = assets.get_font("ARCADECLASSIC",
                                              self.SUB_TITLE_SIZE)
        self.sections = self._build_sections()

    def _build_sections(self) -> list[tuple[pygame.Surface, list[Row]]]:
        """Render every header, key and description once."""
        sections = []
        for header, rows in self.CONTENT.items():
            header_text = self.sub_title_font.render(header, True,
                                                     self.HEADER_COLOR)
            rendered: list[Row] = []
            for key, description in rows:
                key_text = self.text_font.render(key, True, self.KEY_COLOR)
                desc_text = self.text_font.render(description, True,
                                                  self.TEXT_COLOR)
                rendered.append((key_text, desc_text))
            sections.append((header_text, rendered))
        return sections

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        """Return BACK when Enter is pressed, NONE otherwise."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return ScreenAction.BACK
        return ScreenAction.NONE

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the title, every section and the back button.

        Args:
            surface: The pygame surface to be drawn on.
        """
        width, height = surface.get_size()
        margin = int(width * self.MARGIN_RATIO)
        desc_x = int(width * self.DESC_X_RATIO)

        title = self.draw_title(surface, self.TITLE_TEXT,
                                self.sub_title_font, self.HEADER_COLOR,
                                (width // 2, int(height * self.TITLE_Y_RATIO)),
                                shadow_color=self.SHADOW_COLOR)
        y = title.bottom + self.TITLE_GAP

        for header, rows in self.sections:
            rect = header.get_rect(topleft=(margin, y))
            surface.blit(header, rect)
            pygame.draw.line(surface, self.HEADER_COLOR,
                             (margin, rect.bottom + 4),
                             (width - margin, rect.bottom + 4), 2)
            y = rect.bottom + 16

            for key, description in rows:
                surface.blit(key, (margin + self.INDENT, y))
                surface.blit(description, (desc_x, y))
                y += self.LINE_HEIGHT
            y += self.SECTION_GAP

        self._draw_back_button(surface)
