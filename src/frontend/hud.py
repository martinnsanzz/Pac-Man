# Built-in modules
from math import ceil

# Installed modules
import pygame

# Local modules
from .assets import AssetsLoader, Fruit


class HUD():
    """Draw the in-game HUD: lives, collected fruits, score and timer.

    Args:
        assets: Loader providing the font, HUD icons and fruit icons.

    Attributes:
        assets: Loader providing the font, HUD icons and fruit icons.
        font: Font used to render every text element.
    """
    PAD = 10
    FONT_SIZE = 40
    TXT_COLOR = (255, 255, 255)
    MAX_LIFE_ICONS = 3
    MAX_FRUITS_ICONS = 7
    COUNTER_Y_OFFSET = 5

    def __init__(self, assets: AssetsLoader):
        self.assets = assets
        self.font = assets.get_font("DIGITAL808", self.FONT_SIZE)

    def display_hud(self, surface: pygame.Surface, lives: int,
                    fruits: list[Fruit], score: int, high_score: int,
                    time_left: int) -> None:
        """Draw every HUD element onto `surface`.

        Args:
            surface: Surface to draw on.
            lives: Number of remaining lives.
            fruits: Collected fruits in collection order, oldest first.
            score: Current score.
            high_score: Highest score reached.
            time_left: Time remaining, in seconds.
        """
        self._display_lives(surface, lives)
        self._display_fruits(surface, fruits)
        self._display_score(surface, score)
        self._display_high_score(surface, high_score)
        self._display_time_left(surface, time_left)

    def _display_lives(self, surface: pygame.Surface, lives: int) -> None:
        """Draw the remaining lives in the bottom-left corner.

        Draw one life icon per remaining life, left to right, up to
        ``MAX_LIFE_ICONS``. If ``lives`` exceeds that limit, draw a text
        counter (``x<lives>``) before the icons.

        Args:
            surface: Surface to draw on.
            lives: Number of remaining lives.
        """
        icon = self.assets.hud_icons["LIVE"]
        step = self.assets.SCALED_HUD + self.PAD
        x = self.PAD
        y = surface.get_height() - step

        if lives > self.MAX_LIFE_ICONS:
            counter = self.font.render(f"x{lives}", True, self.TXT_COLOR)
            surface.blit(counter, (x, y + self.COUNTER_Y_OFFSET))
            x += counter.get_width() + self.PAD

        for _ in range(min(lives, self.MAX_LIFE_ICONS)):
            surface.blit(icon, (x, y))
            x += step

    def _display_fruits(self, surface: pygame.Surface,
                        collected_fruits: list[Fruit]) -> None:
        """Draw the most recently collected fruits in the bottom-right corner.

        Draw at most ``MAX_FRUITS_ICONS`` icons, right to left, starting
        with the most recently collected fruit at the right edge.

        Args:
            surface: Surface to draw on.
            collected_fruits: Collected fruits in collection order, oldest
                first.
        """
        step = self.assets.SCALED_HUD + self.PAD
        x = surface.get_width() - step
        y = surface.get_height() - step

        for fruit in reversed(collected_fruits[-self.MAX_FRUITS_ICONS:]):
            surface.blit(self.assets.fruit_icons[fruit], (x, y))
            x -= step

    def _draw_stat(self, surface: pygame.Surface, label: str, value: str,
                   anchor: str, pos: tuple[int, int]) -> None:
        """Draw a label with its value centred right below it.

        Args:
            surface: Surface to draw on.
            label: Text drawn at ``pos``.
            value: Text drawn below the label, centred on it.
            anchor: ``pygame.Rect`` attribute that ``pos`` refers to
                (``"topleft"``, ``"midtop"`` or ``"topright"``).
            pos: Position of the label's ``anchor`` point, in pixels.
        """
        label_surf = self.font.render(label, True, self.TXT_COLOR)
        value_surf = self.font.render(value, True, self.TXT_COLOR)
        label_rect = label_surf.get_rect(**{anchor: pos})
        value_rect = value_surf.get_rect(midtop=label_rect.midbottom)

        surface.blit(label_surf, label_rect)
        surface.blit(value_surf, value_rect)

    def _display_score(self, surface: pygame.Surface, score: int) -> None:
        """Draw the score label and current score at the top-left."""
        self._draw_stat(surface, "Score", str(score),
                        "topleft", (self.PAD, self.PAD))

    def _display_high_score(self, surface: pygame.Surface,
                            high_score: int) -> None:
        """Draw the high score label and value at the top-centre."""
        self._draw_stat(surface, "High Score", str(high_score),
                        "midtop", (surface.get_width() // 2, self.PAD))

    def _display_time_left(self, surface: pygame.Surface,
                           time_left: float) -> None:
        """Draw the time-left label and countdown at the top-right."""
        seconds = max(0, ceil(time_left))
        self._draw_stat(surface, "Time left", str(seconds),
                        "topright", (surface.get_width() - self.PAD, self.PAD))
