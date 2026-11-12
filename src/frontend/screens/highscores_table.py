# Installed modules
import pygame

# Local modules
from .actions import ScreenAction
from .screen import Screen
from ..assets import AssetsLoader
from ...backend import Highscores


class HighscoresTable(Screen):
    """Highscores screen with sorted entries.

    Attributes:
        highscores: The table of entries to display.
    """
    TITLE_Y_RATIO = 0.15
    TITLE_GAP = 70
    LINE_HEIGHT = 32
    ROW_HEIGHT = 40
    HEADER_COLOR = (255, 255, 0)

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader, highscores: Highscores) -> None:
        super().__init__(screen_w, screen_h, assets)
        self.highscores = highscores
        self.sub_title_font = assets.fonts["ARCADETITLE"]
        self.row_font = assets.fonts["DIGITAL808"]

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        """Handle a single pygame event for the Highscores screen.

        Enter to go back or Escape to quit the game.

        Args:
            event: The pygame event to process.

        Returns:
            The action to return or Action.NONE otherwise.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return ScreenAction.BACK
        return ScreenAction.NONE

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the Highscores screen on the surface.

        Args:
            surface: The pygame surface to be drawn on.
        """
        # ---------- title ----------
        margin_x = surface.get_width() // 8
        y = surface.get_height() * self.TITLE_Y_RATIO

        title = self.sub_title_font.render(
                "HIGHSCORES", True, self.HEADER_COLOR)
        surface.blit(title, title.get_rect(midleft=(margin_x, y)))
        y += self.TITLE_GAP

        # ---------- rows ----------
        width = surface.get_width()
        for rank, entry in enumerate(self.highscores.table, start=1):
            rank_text = self.row_font.render(f"{rank}.", True,
                                             self.SELECTED_COLOR)
            name_text = self.row_font.render(entry.name, True,
                                             self.SELECTED_COLOR)
            score_text = self.row_font.render(str(entry.score), True,
                                              self.SELECTED_COLOR)

            surface.blit(rank_text, rank_text.get_rect(
                midleft=(width * 0.15, y)))
            surface.blit(name_text, name_text.get_rect(
                midleft=(width * 0.30, y)))
            surface.blit(score_text, score_text.get_rect(
                midleft=(width * 0.65, y)))
            y += self.ROW_HEIGHT
