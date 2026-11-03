# Built-in
from argparse import ArgumentParser, ArgumentError, Namespace


def json_file(file: str) -> str:
    if not file.lower().endswith(".json"):
        raise ArgumentError(None,
                            f"{file} isn't a valid json file.")
    return file


def load_arguments() -> Namespace:
    parser = ArgumentParser(description="Read a file from CLI")

    parser.add_argument("file", type=json_file)

    try:
        known, unknown = parser.parse_known_args()
    except ArgumentError as e:
        msg = str(e)
        raise ArgumentError(None, msg.capitalize()) from e

    if unknown:
        raise ArgumentError(None, "Incorrect argument on command line:\n   -"
                                  "Correct usage: uv run python pac-man.py "
                                  "config.json")
    return known
