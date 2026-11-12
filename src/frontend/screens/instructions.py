# Installed modules
import pygame

# Local modules
from .actions import ScreenAction
from .screen import Screen
from ..assets import AssetsLoader

# TODO: read values of pacgums from config


class Instructions(Screen):
    """Instructions screen with commands and cheat codes."""
    TITLE_Y_RATIO = 0.15
    TITLE_GAP = 70
    SUB_TITLE_SIZE = 50
    LINE_HEIGHT = 32
    SECTION_GAP = 20
    HEADER_COLOR = (255, 255, 0)

    CONTENT: dict[str, tuple[str, ...]] = {
        "CONTROLS": ("Arrows / 'WASD': move Pac-Man",
                     "'p': pause/unpause",
                     "'esc': quit the game"),
        "RULES": ("Pacgums: Give points",
                  "Super-Pacgums: Give points & lets Pac-Man eat ghosts"),
        "CHEAT CODES": ("TODO",)
        }

    def __init__(self, screen_w: int, screen_h: int,
                 assets: AssetsLoader) -> None:
        super().__init__(screen_w, screen_h, assets)
        self.sub_title_font = assets.fonts["ARCADETITLE"]

    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        """Handle a single pygame event for the Instructions screen.

        Enter to go back or Escape to quit the game.

        Args:
            event: The pygame event to process.

        Returns:
            The action to return or Action.PASS otherwise.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return ScreenAction.BACK
        return ScreenAction.NONE

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the instructions screen on the surface.

        Args:
            surface: The pygame surface to be drawn on.
        """
        # ---------- title ----------
        margin_x = surface.get_width() // 8
        y = surface.get_height() * self.TITLE_Y_RATIO

        title = self.sub_title_font.render(
                "INSTRUCTIONS", True, self.HEADER_COLOR)
        surface.blit(title, title.get_rect(midleft=(margin_x, y)))
        y += self.TITLE_GAP

        # --------- instructions ----------
        for header, lines in self.CONTENT.items():
            text = self.sub_title_font.render(header, True, self.HEADER_COLOR)
            surface.blit(text, text.get_rect(midleft=(margin_x, y)))
            y += self.LINE_HEIGHT

            for line in lines:
                text = self.text_font.render(line, True, (255, 255, 255))
                surface.blit(text, text.get_rect(midleft=(margin_x, y)))
                y += self.LINE_HEIGHT

            y += self.SECTION_GAP

        # ---------- back button ----------
        text = self.button_font.render("Back", True, self.SELECTED_COLOR)
        rect = text.get_rect(center=(surface.get_width() // 2, y))
        box = rect.inflate(self.BOX_PADDING_X, self.BOX_PADDING_Y)
        pygame.draw.rect(surface, self.SELECTED_COLOR, box,
                         width=2, border_radius=self.BORDER_RADIUS)
        surface.blit(text, rect)
