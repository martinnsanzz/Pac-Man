# Built-in modules
from sys import stderr, stdout

RGB = tuple[int, int, int]

COLORS: dict[str, RGB] = {
        "black": (0, 0, 0), "blue": (0, 0, 255), "brown": (153, 51, 0),
        "crimson": (204, 0, 51), "cyan": (0, 255, 255),
        "darkred": (102, 0, 0), "gold": (255, 204, 0),
        "lime": (0, 255, 0), "magenta": (255, 0, 255),
        "maroon": (51, 0, 0), "orange": (255, 153, 0),
        "purple": (102, 0, 102), "red": (255, 0, 0),
        "violet": (204, 102, 204), "yellow": (255, 255, 0),
        "green": (153, 204, 102), "gray": (102, 102, 102),
        }

DEFAULT_HUB_COLOR = (102, 102, 102)

RESET = "\033[0m"
BOLD = "\033[1m"

ERROR = "------ERROR FOUND------"


class TerminalPrinter:
    """Print text the terminal using ANSI colors.

    No instance state is used, so the class is a namespace and is not
    meant to be instantiated.
    """
    @classmethod
    def print_msg(cls, msg: str, color: str = "None") -> None:
        """Print a message to stdout in the specified color.

        If color is not present in `COLORS` it will provide a default
        hub color `grey`.
        """
        if not stdout.isatty():
            print(msg)
        if color in COLORS:
            print(f"{cls.build_ansi(COLORS[color])}{msg}{RESET}")
        else:
            print(f"{cls.build_ansi(DEFAULT_HUB_COLOR)}{msg}{RESET}")

    @classmethod
    def print_error(cls, error: str) -> None:
        """Print an error message to stderr in the specified color.

        If color is not present in `COLORS` it will provide a default
        hub color `grey`.
        """
        if not stderr.isatty():
            print(ERROR, file=stderr)
        red = cls.build_ansi(COLORS["red"])
        print(f"{red}{ERROR}\n{error}{RESET}", file=stderr, end="")

    @staticmethod
    def build_ansi(rgb: RGB) -> str:
        """Build the ANSI escape sequence for a 256-color foreground."""
        r, g, b = (TerminalPrinter._to_cube(c) for c in rgb)
        index = 16 + 36 * r + 6 * g + b
        return f"\033[38;5;{index}m"

    @staticmethod
    def _to_cube(channel: int) -> int:
        """Scale a 0-255 channel to the 0-5 range of the 256-color cube."""
        return (channel * 5 + 127) // 255
