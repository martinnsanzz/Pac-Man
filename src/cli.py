# Built-in modules
from argparse import ArgumentError

# Local moodules
from .exceptions import PacManError
from .frontend import TerminalPrinter, App
from .parsing import parse_game_config, load_arguments, load_json


def main() -> None:
    try:
        run_program()
    except (PacManError, ArgumentError) as e:
        TerminalPrinter.print_error(f"{e}\n")


def run_program() -> None:
    """Load arguments, create a GameConfig model and run the app"""
    args = load_arguments()
    config = parse_game_config(load_json(args.file))

    App(config).run()
