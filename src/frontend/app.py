# Built-in modules
from pathlib import Path

# Installed modules
import pygame

# Local modules
from .screens import (MainMenu, ScreenAction, Screen,
                      Instructions, Game, HighscoresTable, Pause,
                      GameOver, Win, EndMenu)
from .assets import AssetsLoader
from ..constants import ARCADE_WIDTH, ARCADE_HEIGHT
from ..exceptions import HighScoreError
from ..validation import GameConfig
from ..backend import Highscores, DevLog, LogKind, CheatCodes
from .log_panel import LogPanel, LogInput


class App:
    """Pygame window that plays the game and handles user input.

    Attributes:
        game_config: Configuration of game extracted from config.json
        clock: Pygame clock.
        screen: Pygame window to hold the drawings.
        arcade_screen: Subwindow to hold arcade related drawings.
        canvas: Surface CANVAS_H tall, as wide as the window screen.
        canvas_size: Canvas scaled by the user screen.
        canvas_w: Width size of the canvas surface.
        log_rect: Rect for the log window.
        arcade_rect: Rect for the arcade window.
        side_rect: Rect for the side window.
        assets: Loader holding every font, sprite and sound.
        dev_log: Warnings, messages and the input line of the dev log.
        cheats: Cheat code lookup and the toggles currently active.
        log_panel: Draws the dev log on the left side of the canvas.
        highscores: Persistent highscore table, loaded at startup.
        main_menu: Main menu window to return to.
        current_screen: Current menu or window to be displayed.
        game: Running game, or None when no game is in progress.
        running: False once the main loop must stop.
        on_dev_mode: True while dev mode is open and keys go to the log.
    """

    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    # Canvas
    CANVAS_H = 1080
    LOG_GAP = 16
    ARCADE_W = int(ARCADE_WIDTH * CANVAS_H / ARCADE_HEIGHT)
    ARCADE_DIM = 60

    # Display
    FPS = 60
    BACKGROUND = (12, 14, 16)

    # Screens
    ENDMENUS: dict[ScreenAction, type[EndMenu]] = {
        ScreenAction.GAME_OVER: GameOver,
        ScreenAction.WIN: Win,
    }

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def __init__(self, game_config: GameConfig,
                 dev_log: DevLog) -> None:
        """Open the window, load the assets and the highscores."""
        AssetsLoader.validate_assets()
        self.game_config = game_config

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = self._create_window()
        self._build_canvas()
        self.arcade_screen = pygame.Surface((ARCADE_WIDTH, ARCADE_HEIGHT))

        self.assets = AssetsLoader()
        self.assets.load()

        self.dev_log = dev_log
        self.cheats = CheatCodes()
        self.log_panel = LogPanel(self.assets, self.dev_log)

        self.highscores = self._load_highscores()
        self.main_menu: Screen = MainMenu(self.assets)

        self.current_screen: Screen = self.main_menu
        self.game: Game | None = None
        self.running = True
        self.on_dev_mode = False

    # ------------------------------------------------------------------
    # Window and Canvas
    # ------------------------------------------------------------------
    @staticmethod
    def _create_window() -> pygame.Surface:
        """Open the resizable window, set its title and hide the cursor."""
        pygame.display.set_caption("Pac-Man")
        pygame.mouse.set_visible(False)
        return pygame.display.set_mode((0, 0), pygame.RESIZABLE)

    def _build_canvas(self) -> None:
        """Size the canvas to the window ratio and split it into areas.

        Called at startup and on every resize so the arcade always fills the
        window height and the side panels absorb the extra width.
        """
        win_w, win_h = self.screen.get_size()
        self.canvas_w = max(int(win_w / win_h * self.CANVAS_H),
                            self.ARCADE_W)
        self.canvas = pygame.Surface((self.canvas_w, self.CANVAS_H))
        self.log_rect, self.arcade_rect, self.side_rect = \
            self._compute_layout()
        self.canvas_size = self._compute_canvas_size()

    def _compute_layout(self) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        """Split the canvas into the log, arcade and side areas.

        The arcade keeps its ratio and fills the canvas height. The log and
        side panels share the space left on each side.

        Returns:
            The log, arcade and side rects, in canvas coordinates.
        """
        arcade_x = (self.canvas_w - self.ARCADE_W) // 2

        arcade = pygame.Rect(arcade_x, 0, self.ARCADE_W, self.CANVAS_H)
        log = pygame.Rect(0, 0, arcade.left - self.LOG_GAP, self.CANVAS_H)
        side = pygame.Rect(arcade.right, 0, self.canvas_w - arcade.right,
                           self.CANVAS_H)
        return log, arcade, side

    def _compute_canvas_size(self) -> tuple[int, int]:
        """Return the canvas size scaled to fit the window."""
        win_w, win_h = self.screen.get_size()
        factor = min(win_w / self.canvas_w, win_h / self.CANVAS_H)
        return int(self.canvas_w * factor), int(self.CANVAS_H * factor)

    # ------------------------------------------------------------------
    # Main Loop
    # ------------------------------------------------------------------
    def run(self) -> None:
        """Run the main loop until the window is closed."""
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000
            action = self._handle_events()
            if action == ScreenAction.NONE:
                action = self._update(dt)
            self._switch(action)
            self._draw()
        pygame.quit()

    def _handle_events(self) -> ScreenAction:
        """Forward events to the current screen.

        Returns:
            The first action a screen asked for, or NONE.
        """
        action = ScreenAction.NONE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self._build_canvas()
            if self.on_dev_mode:
                self._handle_dev_input(event)
                continue
            result = self.current_screen.handle_event(event)
            if action == ScreenAction.NONE:
                action = result
        return action

    def _handle_dev_input(self, event: pygame.event.Event) -> None:
        """Pass a key event to the log panel and act on what it asks."""
        match self.log_panel.handle_event(event):
            case LogInput.CLOSE:
                self.dev_log.text = ""
                self.on_dev_mode = False
            case LogInput.SUBMIT:
                self.dev_log.process(self.cheats)

    def _update(self, dt: float) -> ScreenAction:
        """Advance the current screen by dt seconds."""
        return self.current_screen.update(dt)

    def _draw(self) -> None:
        """Draw the screen into the canvas and fit it to the window."""
        self.screen.fill((0, 0, 0))
        self.canvas.fill((0, 0, 0))

        self.log_panel.draw(self.canvas, self.log_rect, self.on_dev_mode)
        self.arcade_screen.fill(self.BACKGROUND)
        self.current_screen.draw(self.arcade_screen)
        if self.on_dev_mode:
            self.arcade_screen.fill(
                    (self.ARCADE_DIM, self.ARCADE_DIM, self.ARCADE_DIM),
                    special_flags=pygame.BLEND_RGB_MULT)

        arcade = pygame.transform.scale(self.arcade_screen,
                                        self.arcade_rect.size)
        self.canvas.blit(arcade, self.arcade_rect)

        scaled = pygame.transform.scale(self.canvas, self.canvas_size)
        self.screen.blit(scaled,
                         scaled.get_rect(
                             center=self.screen.get_rect().center))
        pygame.display.flip()

    # ------------------------------------------------------------------
    # Screen Switching
    # ------------------------------------------------------------------
    def _switch(self, action: ScreenAction | None) -> None:
        """Change the current screen according to the action."""
        match action:
            case ScreenAction.QUIT:
                self.running = False
            case ScreenAction.BACK | ScreenAction.MAIN_MENU:
                self._show_main_menu()
            case ScreenAction.START_GAME:
                self._start_game()
            case ScreenAction.HIGHSCORES:
                self._show_highscores()
            case ScreenAction.INSTRUCTIONS:
                self._show_instructions()
            case ScreenAction.PAUSE:
                self._show_pause()
            case ScreenAction.GAME_OVER | ScreenAction.WIN:
                self._show_end_menu(action)
            case ScreenAction.NAME_SUBMITTED:
                self._insert_high_score()
            case ScreenAction.DEV_MODE:
                self.on_dev_mode = True
            case ScreenAction.RESUME:
                self._resume()

    def _show_main_menu(self) -> None:
        """Drop the current game and go back to the main menu."""
        self.game = None
        self.current_screen = self.main_menu

    def _start_game(self) -> None:
        """Create a new game and make it the current screen."""
        self.game = Game(self.assets, self.game_config,
                         self.highscores.get_high_score())
        self.current_screen = self.game

    def _show_highscores(self) -> None:
        """Show the highscore table."""
        self.current_screen = HighscoresTable(self.assets,
                                              self.highscores)

    def _show_instructions(self) -> None:
        """Show the instructions screen."""
        self.current_screen = Instructions(self.assets)

    def _show_pause(self) -> None:
        """Open the pause menu over the running game."""
        if self.game is None:
            return
        self.current_screen = Pause(ARCADE_WIDTH, ARCADE_HEIGHT, self.assets,
                                    self.game)

    def _show_end_menu(self, action: ScreenAction) -> None:
        """Open the game over or win menu over the finished game."""
        if self.game is None:
            return
        menu = self.ENDMENUS[action]
        is_highscore = self.highscores.is_highscore(self.game.score)
        self.current_screen = menu(ARCADE_WIDTH, ARCADE_HEIGHT, self.assets,
                                   self.game, is_highscore)

    def _resume(self) -> None:
        """Close the pause menu and go back to the game."""
        if self.game is not None:
            self.current_screen = self.game

    # ------------------------------------------------------------------
    # Highscores
    # ------------------------------------------------------------------
    def _load_highscores(self) -> Highscores:
        """Load the highscore table; on failure warn in the dev log."""
        highscores = Highscores(Path(self.game_config.highscores_path))
        try:
            highscores.load()
        except HighScoreError as e:
            self.dev_log.add(str(e), LogKind.WARNING)
        return highscores

    def _save_highscores(self) -> None:
        """Save the highscore table. On failure warn and keep playing.

        The error is shown in the dev log, so the game never crashes over
        a file it cannot write.
        """
        try:
            self.highscores.save()
        except HighScoreError as e:
            self.dev_log.add(str(e), LogKind.WARNING)

    def _insert_high_score(self) -> None:
        """Insert the current score into the table and save it."""
        if self.game is None or not isinstance(self.current_screen,
                                               EndMenu):
            return
        name = self.current_screen.name

        self.highscores.insert(name, self.current_screen.game.score)
        self._save_highscores()
