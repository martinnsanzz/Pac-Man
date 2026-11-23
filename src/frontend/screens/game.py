# Installed modules
import pygame

# Local modules
from .screen import Screen, ScreenAction
from ..assets import AssetsLoader, Fruit
from ..renderers import MazeRenderer, HudRenderer, PlayerRenderer
from ...validation import GameConfig
from ...backend import Level, Player, PlayerDir, TileMap
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
        col, row = self.level.spawn_point
        return Player((int((col + 0.5) * TILE_PX),
                       int((row + 0.5) * TILE_PX)))

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return ScreenAction.PAUSE

            if self.player.direction == PlayerDir.NONE:
                self._move_player(event.key)

            #  temp to be deleted
            if event.key == pygame.K_1:
                self.score += 100
            elif event.key == pygame.K_9:
                return self._advance_level()
        return ScreenAction.NONE

    def _move_player(self, key: int) -> None:
        """Set the player's direction from a pressed key."""
        if key in self.UP_KEYS:
            self.player.direction = PlayerDir.UP
        elif key in self.DOWN_KEYS:
            self.player.direction = PlayerDir.DOWN
        elif key in self.LEFT_KEYS:
            self.player.direction = PlayerDir.LEFT
        elif key in self.RIGHT_KEYS:
            self.player.direction = PlayerDir.RIGHT

    def _advance_level(self) -> ScreenAction:
        """Go to the next level, or win if the last one was just cleared."""
        if self.current_level >= self.last_level:
            return ScreenAction.WIN
        self.current_level += 1
        self.level = Level(self.config, self.current_level)
        return ScreenAction.NONE

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update(self, dt: float) -> ScreenAction:
        """Update level timer and check game status."""
        self.level.update(dt)
        self.player.update(dt)

        if self.player.direction != PlayerDir.NONE:
            self._check_player()
        return self._check_game_status()

    def _check_player(self) -> None:
        x, y = self.player.pos_x, self.player.pos_y
        col, row = TileMap.pixel_to_tile(x, y)

        if not self.level.has_wall(col, row, self.player.direction):
            return

        center = TileMap.tile_center(col, row)

        if self.player.has_reached(center):
            self.player.center_pos_to_cell(center)
            self.player.direction = PlayerDir.NONE

    def _check_game_status(self) -> ScreenAction:
        if self.level.time_left <= 0:
            return ScreenAction.GAME_OVER
        return ScreenAction.NONE

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface) -> None:
        self._draw_level(surface)
        self.player_renderer.display_player(surface, self.player)

        self.hud_renderer.display_hud(surface, self.lives,
                                      self.fruits_collected,
                                      self.score, self.highscore,
                                      self.level.time_left,
                                      self.current_level, self.last_level)

    def _draw_level(self, surface: pygame.Surface) -> None:
        """Draw the maze of the current level."""
        self.maze_renderer.render_maze(surface, self.level.grid)
