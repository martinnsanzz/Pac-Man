# Built-in modules
from enum import Enum, auto


class PlayerDir(Enum):
    """Enumerate the directions in which the player can move.

    Attributes:
        UP: Towards the top of the maze.
        DOWN: Towards the bottom of the maze.
        LEFT: Towards the left of the maze.
        RIGHT: Towards the right of the maze.
        NONE: No direction; the player is standing still.
    """
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @property
    def opposite(self) -> "PlayerDir":
        """Return the opposite direction.

        Returns:
            The direction facing the other way. ``NONE`` has no opposite
            and returns ``NONE``.
        """
        return _OPPOSITES.get(self, PlayerDir.NONE)


# Pairs of opposite directions, used by ``PlayerDir.opposite``.
_OPPOSITES: dict[PlayerDir, PlayerDir] = {
    PlayerDir.UP: PlayerDir.DOWN,
    PlayerDir.DOWN: PlayerDir.UP,
    PlayerDir.LEFT: PlayerDir.RIGHT,
    PlayerDir.RIGHT: PlayerDir.LEFT,
}


class PlayerState(Enum):
    MOVING = auto()
    DEAD = auto()
    IDLE = auto()


class LogKind(Enum):
    """Category of a log entry, used by the UI to pick its color.

    Attributes:
    INFO: General information about the game.
    WARNING: Something went wrong or an input was not understood.
    CHEAT: Feedback from a successfully applied cheat code.
    MESSAGE: Plain text typed by the user.
    """
    INFO = auto()
    WARNING = auto()
    CHEAT = auto()
    MESSAGE = auto()


class Cheat(Enum):
    """Cheats that can be activated by typing their code.

    Each member's value is the code the player must type, after a
    leading ``/``. Cheats in ``CheatCodes.ONE_SHOTS`` take effect once,
    all the others are toggles.
    """
    # Toggles: stay on until typed again or cleared with NOCHEATS
    IMMORTAL = "IMMORTAL"
    ZOOMZOOM = "ZOOMZOOM"
    FREEZEUP = "FREEZEUP"

    # One-shots: applied once when typed
    SKIPZONE = "SKIPZONE"
    MORELIFE = "MORELIFE"
    SUPERPAC = "SUPERPAC"
    NOCHEATS = "NOCHEATS"
