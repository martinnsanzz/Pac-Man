# Built-in modules
from argparse import ArgumentError
from pathlib import Path

# Local moodules
from .exceptions import PacManError
from .frontend import TerminalPrinter
from .parsing import load_arguments, load_json, parse_game_config


def main() -> None:
    try:
        config = load_json(Path(load_arguments().file))
        game_config = parse_game_config(config)
        print(game_config)
    except (PacManError, ArgumentError) as e:
        TerminalPrinter.print_error(f"{e}\n")
