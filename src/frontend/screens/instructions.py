# Installed modules
import pygame

# Local modules
from .action import Action
from .screen import (Screen, SUB_FONT_PATH, SELECTED_COLOR, BORDER_RADIUS,
                     BOX_PADDING_Y, BOX_PADDING_X, TEXT_COLOR)

# ---------- UI ----------
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
        "RULES": ("Pacgums: 10 points",
                  "Super-Pacgums: 50 points & opens a window to eat ghosts"),
        "CHEAT CODES": ("TODO",)
        }


class Instructions(Screen):
    """Instructions screen with commands and cheat codes."""
    def __init__(self) -> None:
        super().__init__()
        self.sub_title_font = pygame.font.Font(
                SUB_FONT_PATH, SUB_TITLE_SIZE)

    def handle_event(self, event: pygame.event.Event) -> Action:
        """Handle a single pygame event for the Instructions screen.

        Enter to go back or Escape to quit the game.

        Args:
            event: The pygame event to process.

        Returns:
            The action to return or Action.PASS otherwise.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return Action.BACK
        return Action.PASS

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the instructions screen on the surface.

        Args:
            surface: The pygame surface to be drawn on.
        """
        # ---------- title ----------
        margin_x = surface.get_width() // 8
        y = surface.get_height() * TITLE_Y_RATIO

        title = self.sub_title_font.render(
                "INSTRUCTIONS", True, HEADER_COLOR)
        surface.blit(title, title.get_rect(midleft=(margin_x, y)))
        y += TITLE_GAP

        # --------- instructions ----------
        for header, lines in CONTENT.items():
            text = self.sub_title_font.render(header, True, HEADER_COLOR)
            surface.blit(text, text.get_rect(midleft=(margin_x, y)))
            y += LINE_HEIGHT

            for line in lines:
                text = self.text_font.render(line, True, (255, 255, 255))
                surface.blit(text, text.get_rect(midleft=(margin_x, y)))
                y += LINE_HEIGHT

            y += SECTION_GAP

        # ---------- back button ----------
        text = self.sub_font.render("Back", True, SELECTED_COLOR)
        rect = text.get_rect(center=(surface.get_width() // 2, y))
        box = rect.inflate(BOX_PADDING_X, BOX_PADDING_Y)
        pygame.draw.rect(surface, SELECTED_COLOR, box,
                         width=2, border_radius=BORDER_RADIUS)
        surface.blit(text, rect)
        keys = self.text_font.render("ENTER: BACK    ESC: QUIT",
                                     True, TEXT_COLOR)
        rect = keys.get_rect(center=(surface.get_width() // 2,
                                     y + LINE_HEIGHT * 1.15))
        surface.blit(keys, rect)
