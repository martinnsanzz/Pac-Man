# Installed modules
try:
    import mazegen  # type: ignore [unused-ignore]
except (ModuleNotFoundError, ImportError):
    mazegen = None

# Local modules
from ..validation import GameConfig
from ..constants import MAZE_COLS, MAZE_ROWS
from ..exceptions import MazegenError


class Level():
    """Represent a game level with a generated maze and a countdown timer.

    The maze is generated on construction through the ``mazegen``
    library. The remaining time is decreased in whole seconds by
    accumulating frame deltas via ``decrease_timer``.

    Attributes:
        time_left: Remaining time for the level, initialised from
            ``config.level_time_limit`` and decremented by 1 per elapsed
            second.
        grid: Two-dimensional maze grid produced by ``gen_maze``.
        start_time: Time in seconds accumulated towards the next
            one-second timer tick.
    """
    def __init__(self, config: GameConfig, level: int) -> None:
        """Initialize the level timer and generate its maze.

        Args:
            config: Game configuration providing ``level_time_limit``.
            level: Level number used to select the maze seed, or None for
                a randomly seeded maze.

        Raises:
            MazegenError: If the ``mazegen`` library is not available.
        """
        self.time_left = config.level_time_limit
        self.grid = self.gen_maze(level)
        self.start_time = 0.0
        self.spawn_point = (MAZE_COLS // 2, MAZE_ROWS // 2)

    def update(self, dt: float) -> None:
        """Update the level state for a time step.

        Args:
            dt: Time elapsed since the previous update in seconds.
        """
        self._decrease_timer(dt)

    def _decrease_timer(self, dt: float) -> None:
        """Advance the level timer by a time delta.

        Accumulate ``dt`` in ``start_time``. Once at least one second has
        accumulated, subtract one second from the accumulator (keeping the
        remainder) and decrease ``time_left`` by 1.

        Args:
            dt: Time elapsed since the previous call, in seconds.
        """
        self.start_time += dt

        if self.start_time >= 1.0:
            self.start_time -= 1.0
            self.time_left -= 1

    @staticmethod
    def gen_maze(level: int) -> list[list[int]]:
        """Generate a maze grid for the given level.

        Use a fixed seed (42) for level 1 so that its maze is
        reproducible. For any other value, the generator
        receives no seed.

        Args:
            level: Level number, or None for an unseeded maze.

        Returns:
            The generated maze as a two-dimensional list of integers, with
            ``MAZE_ROWS`` x ``MAZE_COLS`` dimensions as passed to the
            generator.

        Raises:
            MazegenError: If the ``mazegen`` library is not available.
        """
        if not mazegen:
            raise MazegenError("Level can't be loaded. Missing mazegen "
                               "library on 'venv'")
        seed = 42 if level == 1 else None
        generator = mazegen.MazeGenerator(MAZE_COLS, MAZE_ROWS,
                                          (0, 0), (1, 1), False,
                                          seed)
        generator.generate()
        grid: list[list[int]] = generator.maze
        return grid
