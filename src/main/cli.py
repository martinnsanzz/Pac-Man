# Built-in modules

# Local moodules
from .exceptions import PacManError
from .frontend import TerminalPrinter


def main() -> None:
    try:
        print("Hello")
    except (PacManError) as e:
        TerminalPrinter.print_error(f"{e}\n")
