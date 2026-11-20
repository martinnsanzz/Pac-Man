# Built-in modules
from pathlib import Path

# Installed modules
import pygame

# Local modules
from .screens import (MainMenu, ScreenAction, Screen,
                      Instructions, Game, HighscoresTable, Pause,
                      GameOver, Win, EndMenu)
from .paths import FontsPaths, SpritesPaths, TilemapPath, SfxPaths, HudPaths
from .assets import AssetsLoader
from .terminal import TerminalPrinter
from ..exceptions import LoadAssetsError, PacManError
from ..validation import GameConfig
from ..backend import Highscores, DevLog, LogKind, CheatCodes, Cheat
from .log_panel import LogPanel


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
        highscores: Persistent highscore table, loaded at startup.
        main_menu: Main menu window to return to.
        current_screen: Current menu or window to be displayed.
        game: Running game, or None when no game is in progress.
        running: False once the main loop must stop.
    """
    # Canvas
    CANVAS_H = 1080
    LOG_GAP = 16

    # Arcade screen
    WIDTH = 672
    HEIGHT = 864
    ARCADE_W = int(WIDTH * CANVAS_H / HEIGHT)
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
    def __init__(self, game_config: GameConfig) -> None:
        """Open the window, load the assets and highscore"""
        self.validate_assets()
        self.game_config = game_config

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = self._create_window()
        self.arcade_screen = pygame.Surface((self.WIDTH, self.HEIGHT))
        self._build_canvas()

        self.assets = AssetsLoader()
        self.assets.load()
        self.highscores = self._load_highscores()

        self.dev_log = DevLog()
        self.log_panel = LogPanel(self.assets, self.dev_log)

        self.main_menu: Screen = MainMenu(self.WIDTH,
                                          self.HEIGHT,
                                          self.assets)
        self.current_screen: Screen = self.main_menu
        self.game: Game | None = None
        self.running = True
        self.on_dev_mode = False

        self.cheats = CheatCodes()

    @staticmethod
    def validate_assets() -> None:
        """Raise LoadAssetsError listing every missing asset."""
        missing: list[str] = []
        for paths in (FontsPaths, SpritesPaths, TilemapPath, SfxPaths,
                      HudPaths):
            missing += paths.validate()
        if missing:
            raise LoadAssetsError(
                "Missing assets needed to run pac-man:\n - "
                + "\n - ".join(missing))

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

    def _compute_canvas_size(self) -> tuple[int, int]:
        """Return the canvas size scaled to fit the window."""
        win_w, win_h = self.screen.get_size()
        factor = min(win_w / self.canvas_w, win_h / self.CANVAS_H)
        return int(self.canvas_w * factor), int(self.CANVAS_H * factor)

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

    def _load_highscores(self) -> Highscores:
        """Load the highscore table; on failure print the error and go on."""
        highscores = Highscores(Path(self.game_config.highscores_path))
        try:
            highscores.load()
        except PacManError as e:
            TerminalPrinter.print_error(f"{e}\n")
        return highscores

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self) -> None:
        """Run the main loop until the window is closed."""
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000
            self._handle_events()
            self._update(dt)
            self._draw()
        pygame.quit()

    def _handle_events(self) -> None:
        """Read the pygame events and forward them to the screen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self._build_canvas()
            if self.on_dev_mode:
                self._handle_dev_input(event)
                continue
            self._switch(self.current_screen.handle_event(event))

    def _update(self, dt: float) -> None:
        """Advance the current screen by dt seconds."""
        self.current_screen.update(dt)

    def _draw(self) -> None:
        """Draw the screen into the canvas and fit it to the window."""
        self.screen.fill((0, 0, 0))
        self.canvas.fill((0, 0, 0))

        self.log_panel.draw(self.canvas, self.log_rect, self.on_dev_mode)
        self.arcade_screen.fill(self.BACKGROUND)
        self.current_screen.draw(self.arcade_screen)

        arcade = pygame.transform.scale(self.arcade_screen,
                                        self.arcade_rect.size)
        self.canvas.blit(arcade, self.arcade_rect)

        scaled = pygame.transform.scale(self.canvas, self.canvas_size)
        self.screen.blit(scaled,
                         scaled.get_rect(
                             center=self.screen.get_rect().center))
        pygame.display.flip()

    # ------------------------------------------------------------------
    # Screen switching
    # ------------------------------------------------------------------
    def _switch(self, action: ScreenAction | None) -> None:
        """Change the current screen according to the action."""
        match action:
            case ScreenAction.QUIT:
                self.highscores.save()
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
                self._enter_dev_mode()
            case ScreenAction.RESUME:
                self._resume()

    def _show_main_menu(self) -> None:
        """Drop the current game and go back to the main menu."""
        self.game = None
        self.current_screen = self.main_menu

    def _start_game(self) -> None:
        """Create a new game and make it the current screen."""
        self.game = Game(self.WIDTH, self.HEIGHT, self.assets,
                         self.game_config, self.highscores.get_high_score())
        self.current_screen = self.game

    def _show_highscores(self) -> None:
        """Show the highscore table."""
        self.current_screen = HighscoresTable(self.WIDTH, self.HEIGHT,
                                              self.assets, self.highscores)

    def _show_instructions(self) -> None:
        """Show the instructions screen."""
        self.current_screen = Instructions(self.WIDTH, self.HEIGHT,
                                           self.assets)

    def _show_pause(self) -> None:
        """Open the pause menu over the running game."""
        if self.game is None:
            return
        self.current_screen = Pause(self.WIDTH, self.HEIGHT, self.assets,
                                    self.game)

    def _show_end_menu(self, action: ScreenAction) -> None:
        """Open the game over or win menu over the finished game."""
        if self.game is None:
            return
        menu = self.ENDMENUS[action]
        is_highscore = self.highscores.is_highscore(self.game.score)
        self.current_screen = menu(self.WIDTH, self.HEIGHT, self.assets,
                                   self.game, is_highscore)

    def _insert_high_score(self) -> None:
        """Inserts current score to highscore if its valid"""
        if self.game is None or not isinstance(self.current_screen,
                                               EndMenu):
            return
        name = self.current_screen.name

        self.highscores.insert(name, self.current_screen.game.score)

    def _resume(self) -> None:
        """Close the pause menu and go back to the game."""
        if self.game is not None:
            self.current_screen = self.game

    # ------------------------------------------------------------------
    # Dev panel
    # ------------------------------------------------------------------

    def _enter_dev_mode(self) -> None:
        """Open dev mode: keys now go to the log input line."""
        self.on_dev_mode = True

    def _exit_dev_mode(self) -> None:
        """Closes dev mode and discard any half-typed input."""
        self.dev_log.text = ""
        self.on_dev_mode = False

    def _handle_dev_input(self, event: pygame.event.Event) -> None:
        """Send a key event to the log input line while dev mode is open.

        Ctrl+T or Escape closes dev mode, Enter submits the line,
        Backspace deletes and any other key types its character.

        Args:
            event: The pygame event to process.
        """
        if event.type != pygame.KEYDOWN:
            return

        ctrl_t = event.mod & pygame.KMOD_CTRL and event.key == pygame.K_t
        if ctrl_t or event.key == pygame.K_ESCAPE:
            self._exit_dev_mode()
        elif event.key == pygame.K_RETURN:
            self._submit_dev_text()
        elif event.key == pygame.K_BACKSPACE:
            self.dev_log.backspace()
        else:
            self.dev_log.add_char(event.unicode)

    def _submit_dev_text(self) -> None:
        """Submit the input line and log the result.

        Text starting with / is checked as a cheat code.
        Empty input does nothing.
        """
        text = self.dev_log.submit()
        if text == "":
            return
        elif not text.startswith("/"):
            self.dev_log.add(text, LogKind.MESSAGE)
        else:
            cheat = self.cheats.submit(text)
            if cheat is None:
                self.dev_log.add(f"Unknown code: {text}", LogKind.WARNING)
            else:
                self.dev_log.add(self._cheat_feedback(cheat), LogKind.CHEAT)

    def _cheat_feedback(self, cheat: Cheat) -> str:
        """Return the log message describing what a submitted cheat did.

        Args:
            cheat: The cheat that was submitted.

        Returns:
            "<CODE> used" for one-shots, otherwise "<CODE> ON"
            or "<CODE> OFF" depending on its status.
        """
        if cheat in CheatCodes.ONE_SHOTS:
            return f"<{cheat.name}> used"
        elif self.cheats.is_active(cheat):
            return f"<{cheat.name}> ON"
        else:
            return f"<{cheat.name}> OFF"
