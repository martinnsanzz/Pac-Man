# Built-in modules
from argparse import ArgumentError
from pathlib import Path

# Local moodules
from .exceptions import PacManError
from .frontend import TerminalPrinter
from .frontend import App


def main() -> None:
    try:
        App().run()
    except (PacManError, ArgumentError) as e:
        TerminalPrinter.print_error(f"{e}\n")
