# Built-in modules

# Installed modules
import pygame

# Local modules
from .screen import Screen, ScreenAction
from ..assets import AssetsLoader, Fruit
from ..renderers import MazeRenderer, HudRenderer, PlayerRenderer
from ...validation import GameConfig
from ...backend import Level, Player


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

        # Objects
        self.player = Player()

        # Renderers
        self.hud_renderer = HudRenderer(assets)
        self.maze_renderer = MazeRenderer(assets)
        self.player_renderer = PlayerRenderer(assets)

        # Persists across levels
        self.last_level = config.total_levels
        self.current_level = 1
        self.lives = config.lives
        self.score = 0
        self.highscore = highscore
        self.fruits_collected: list[Fruit] = [Fruit.APPLE] * 7  # temp

        # Thrown away and rebuilt every level
        self.level = Level(self.config, self.current_level)

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event) -> ScreenAction:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return ScreenAction.PAUSE
            #  temp to be deleted
            elif event.key == pygame.K_1:
                self.score += 100
            elif event.key == pygame.K_9:
                return self._advance_level()
        return ScreenAction.NONE

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
        self.level.decrease_timer(dt)

        return self._check_game_status()

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
