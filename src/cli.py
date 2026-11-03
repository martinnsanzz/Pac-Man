# Built-in modules
from argparse import ArgumentError

# Local moodules
from .exceptions import PacManError
from .frontend import TerminalPrinter


def main() -> None:
    try:
        print("Hello")
    except (PacManError, ArgumentError) as e:
        TerminalPrinter.print_error(f"{e}\n")
