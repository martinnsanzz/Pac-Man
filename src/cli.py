# Built-in modules
from argparse import ArgumentError
from pathlib import Path
from typing import Any

# Local moodules
from .exceptions import PacManError
from .frontend import TerminalPrinter
from .parsing import load_arguments, load_json, parse_game_config
from .models import GameConfig


# def set_game_config(config: dict[str, Any]) -> GameConfig:
#     return GameConfig.model_validate(
#         highscore_filename=config.get("highscore_filename", default="highscore.txt"),
#         lives=config.get("lives", default=3),
#         total_pacgum=config.get("total_pacgum", 3)
#     )


def main() -> None:
    try:
        config = load_json(Path(load_arguments().file))
        game_config = parse_game_config(config)
        print(game_config)
    except (PacManError, ArgumentError) as e:
        TerminalPrinter.print_error(f"{e}\n")
