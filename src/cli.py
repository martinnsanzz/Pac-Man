# Built-in modules
from argparse import ArgumentError
from pathlib import Path

# Local moodules
from .exceptions import PacManError
from .frontend import TerminalPrinter
from .parsing import load_arguments, load_json


def main() -> None:
    try:
        print(load_json(Path(load_arguments().file)))
    except (PacManError, ArgumentError) as e:
        TerminalPrinter.print_error(f"{e}\n")
