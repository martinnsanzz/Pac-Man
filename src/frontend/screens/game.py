# Installed modules
import pygame

# Local modules
from .screen import Screen, ScreenAction
from ..assets import AssetsLoader, Fruit
from ..renderers import MazeRenderer, HudRenderer, PlayerRenderer
from ...validation import GameConfig
from ...backend import Level, Player, PlayerDir, DevLog
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

            self._handle_player_input(event.key)

            #  temp to be deleted
            if event.key == pygame.K_1:
                self.score += 100
            elif event.key == pygame.K_9:
                return self._advance_level()
        return ScreenAction.NONE

    def _handle_player_input(self, key: int) -> None:
        """Steer the player, or buffer the turn if it is already moving.

        Args:
            key: The pygame key code of the pressed key.
        """
        direction = self._direction_from_key(key)
        if direction is None:
            return
        if self.player.direction == PlayerDir.NONE:
            self.player.direction = direction
        else:
            self.player.buffer_direction = direction

    def _direction_from_key(self, key: int) -> PlayerDir | None:
        """Return the direction a key stands for, or None if it isn't one."""
        if key in self.UP_KEYS:
            return PlayerDir.UP
        if key in self.DOWN_KEYS:
            return PlayerDir.DOWN
        if key in self.LEFT_KEYS:
            return PlayerDir.LEFT
        if key in self.RIGHT_KEYS:
            return PlayerDir.RIGHT
        return None

    def _advance_level(self) -> ScreenAction:
        """Go to the next level, or win if the last one was just cleared.

        If ``current_level`` is already the last level, leave the state
        unchanged. Otherwise, increment ``current_level`` and load a new
        ``Level`` for it and place the player at the spawnpoint.

        Returns:
            ``ScreenAction.WIN`` if ``current_level`` is at or beyond
            ``last_level``, otherwise ``ScreenAction.NONE``.
        """
        if self.current_level >= self.last_level:
            return ScreenAction.WIN
        self.current_level += 1
        self.level = Level(self.config, self.current_level)
        self.player.reset_position(self.level.spawn_point)
        return ScreenAction.NONE

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update(self, dt: float, dev_log: DevLog) -> ScreenAction:
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
        self.player.update(dt, self.level, dev_log)

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
