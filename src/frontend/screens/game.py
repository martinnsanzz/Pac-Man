# Installed modules
import pygame

# Local modules
from .screen import Screen, ScreenAction
from ..assets import AssetsLoader, Fruit
from ..renderers import MazeRenderer, HudRenderer, PlayerRenderer
from ...validation import GameConfig
from ...backend import Level, Player, PlayerDir
from ...constants import TILE_PX


class Game(Screen):
    """Game screen that will run all the core pac-man logic."""
    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def __init__(self, assets: AssetsLoader, config: GameConfig,
                 highscore: int) -> None:
        super().__init__(assets)
        self.config = config
        self.assets = assets

        # Renderers
        self.hud_renderer = HudRenderer(assets)
        self.maze_renderer = MazeRenderer(assets)
        self.player_renderer = PlayerRenderer(assets)

        # Game data
        self.last_level = config.total_levels
        self.current_level = 1
        self.lives = config.lives
        self.score = 0
        self.highscore = highscore
        self.fruits_collected: list[Fruit] = [Fruit.APPLE] * 7  # temp

        # Level
        self.level = Level(self.config, self.current_level)

        # Objects
        self.player = self.init_player()

    def init_player(self) -> Player:
        """Create the player at the level's spawn tile.

        Place the player at the center of the tile given by
        ``level.spawn_point``, converted to integer pixel coordinates.

        Returns:
            A new ``Player`` positioned at the spawn tile center.
        """
        col, row = self.level.spawn_point
        return Player(((col + 0.5) * TILE_PX,
                       (row + 0.5) * TILE_PX))

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        """Handle a pygame event and return the resulting screen action.

        On a key press, return ``ScreenAction.PAUSE`` for the Escape key.
        Otherwise, if the player has no current direction
        (``PlayerDir.NONE``), set the direction from the pressed key.
        Events that are not key presses are ignored.

        Args:
            event: The pygame event to handle.

        Returns:
            ``ScreenAction.PAUSE`` if Escape was pressed, otherwise
            ``ScreenAction.NONE``.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return ScreenAction.PAUSE

            if self.player.direction == PlayerDir.NONE:
                self._handle_player_input(event.key)

            #  temp to be deleted
            if event.key == pygame.K_1:
                self.score += 100
            elif event.key == pygame.K_9:
                return self._advance_level()
        return ScreenAction.NONE

    def _handle_player_input(self, key: int) -> None:
        """Set the player's direction from a pressed key.

        Leave the direction unchanged if the key is not one of the
        direction keys.

        Args:
            key: The pygame key code of the pressed key.
        """
        if key in self.UP_KEYS:
            self.player.direction = PlayerDir.UP
        elif key in self.DOWN_KEYS:
            self.player.direction = PlayerDir.DOWN
        elif key in self.LEFT_KEYS:
            self.player.direction = PlayerDir.LEFT
        elif key in self.RIGHT_KEYS:
            self.player.direction = PlayerDir.RIGHT

    def _advance_level(self) -> ScreenAction:
        """Go to the next level, or win if the last one was just cleared.

        If ``current_level`` is already the last level, leave the state
        unchanged. Otherwise, increment ``current_level`` and load a new
        ``Level`` for it.

        Returns:
            ``ScreenAction.WIN`` if ``current_level`` is at or beyond
            ``last_level``, otherwise ``ScreenAction.NONE``.
        """
        if self.current_level >= self.last_level:
            return ScreenAction.WIN
        self.current_level += 1
        self.level = Level(self.config, self.current_level)
        return ScreenAction.NONE

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update(self, dt: float) -> ScreenAction:
        """Advance the level and the player, then check the game status.

        Update the level state, move the player for the elapsed time, and
        evaluate whether the game is over.

        Args:
            dt: Time elapsed since the previous update (assumed to be in
                seconds).

        Returns:
            ``ScreenAction.GAME_OVER`` if the level time has run out,
            otherwise ``ScreenAction.NONE``.
        """
        self.level.update(dt)
        self.player.update(dt, self.level)

        if self.level.time_left <= 0:
            return ScreenAction.GAME_OVER
        return ScreenAction.NONE

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface) -> None:
        self._draw_level(surface)
        self._draw_player(surface)
        self._draw_hub(surface)

    def _draw_level(self, surface: pygame.Surface) -> None:
        """Draw the level maze on the window"""
        self.maze_renderer.render_maze(surface, self.level.grid)

    def _draw_player(self, surface: pygame.Surface) -> None:
        """Draw the player at its current position on the window"""
        self.player_renderer.display_player(surface, self.player)

    def _draw_hub(self, surface: pygame.Surface) -> None:
        """Draw the hub on the window"""
        self.hud_renderer.display_hud(surface, self.lives,
                                      self.fruits_collected,
                                      self.score, self.highscore,
                                      self.level.time_left,
                                      self.current_level, self.last_level)
