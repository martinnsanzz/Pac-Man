# Built-in modules
from typing import NamedTuple

# Installed modules
import pygame

# Local modules
from .actions import ScreenAction
from .screen import Screen
from ..assets import AssetsLoader
from ...backend import Highscores


class Row(NamedTuple):
    rank: pygame.Surface
    name: pygame.Surface
    score: pygame.Surface


class HighscoresTable(Screen):
    """Display highscore entries as rank, name and score rows.

    Show an empty-state message when there are no entries. Rows follow the
    order of ``highscores.table``.

    Args:
        screen_w: Screen width.
        screen_h: Screen height.
        assets: Loader providing the title and row fonts.
        highscores: Source of the entries to display.

    Attributes:
        row_font: Font used for the rows and the empty-state message.
        title: Pre-rendered "HIGHSCORES" title.
        empty_text: Pre-rendered message shown when there are no entries.
        rows: One ``(rank, name, score)`` tuple of rendered text per entry.
    """
    TITLE_Y_RATIO = 0.15
    TITLE_GAP = 70
    ROW_HEIGHT = 40
    MARGIN_RATIO = 0.125
    RANK_X, NAME_X, SCORE_X = 0.15, 0.30, 0.65
    TITLE_FONT_SIZE = 50
    ROW_FONT_SIZE = 30
    HEADER_COLOR = (255, 255, 0)

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader, highscores: Highscores) -> None:
        super().__init__(screen_w, screen_h, assets)
        title_font = assets.get_font("ARCADECLASSIC", self.TITLE_FONT_SIZE)
        self.row_font = assets.get_font("DIGITAL808", self.ROW_FONT_SIZE)
        self.title = title_font.render("HIGHSCORES", True, self.HEADER_COLOR)
        self.empty_text = self.row_font.render("NO SCORES YET", True,
                                               self.TEXT_COLOR)
        self.rows = self._build_rows(highscores)

    def _build_rows(self, highscores: Highscores) -> list[Row]:
        """Render each entry once as rank, name and score text.

        Args:
            highscores: Source of the entries to render.

        Returns:
            One ``(rank, name, score)`` tuple of rendered surfaces per
            entry, in table order. Ranks start at 1.
        """
        rows = []
        for rank, entry in enumerate(highscores.table, start=1):
            rank_text = self.row_font.render(f"{rank}.", True,
                                             self.SELECTED_COLOR)
            name_text = self.row_font.render(entry.name, True,
                                             self.SELECTED_COLOR)
            score_text = self.row_font.render(str(entry.score), True,
                                              self.SELECTED_COLOR)
            rows.append(Row(rank_text, name_text, score_text))
        highscores.insert("Martin", 200)
        return rows

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        """Return BACK when Enter is pressed, NONE otherwise."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return ScreenAction.BACK
        return ScreenAction.NONE

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the title, the rows or an empty message, and the back button.

        Args:
            surface: Surface to draw on.
        """
        width, height = surface.get_size()
        y = int(height * self.TITLE_Y_RATIO)
        surface.blit(self.title, self.title.get_rect(
            midleft=(int(width * self.MARGIN_RATIO), y)))

        if self.rows:
            self._draw_rows(surface, y + self.TITLE_GAP)
        else:
            surface.blit(self.empty_text, self.empty_text.get_rect(
                center=(width // 2, height // 2)))
        self._draw_back_button(surface)

    def _draw_rows(self, surface: pygame.Surface, y: int) -> None:
        """Draw every row's rank, name and score in aligned columns.

        Column positions are fractions of the surface width (``RANK_X``,
        ``NAME_X``, ``SCORE_X``). Rows are spaced ``ROW_HEIGHT`` apart.

        Args:
            surface: Surface to draw on.
            y: Vertical position of the first row.
        """
        columns = (self.RANK_X, self.NAME_X, self.SCORE_X)
        for row in self.rows:
            for text, ratio in zip(row, columns):
                surface.blit(text, text.get_rect(
                    midleft=(int(surface.get_width() * ratio), y)))
            y += self.ROW_HEIGHT
