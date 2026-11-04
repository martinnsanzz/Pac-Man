# Built-in
from argparse import ArgumentParser, ArgumentError, Namespace


def json_file(file: str) -> str:
    if not file.lower().endswith(".json"):
        raise TypeError(f"'{file}' isn't a valid json file.")
    return file


def load_arguments() -> Namespace:
    parser = ArgumentParser(description="Read a file from CLI",
                            exit_on_error=False)

    parser.add_argument("file")

    try:
        known, unknown = parser.parse_known_args()

        json_file(known.file)
    except TypeError as e:
        raise ArgumentError(None, str(e)) from e
    except ArgumentError:
        raise ArgumentError(None, "Missing config file in CLI.")

    if unknown:
        raise ArgumentError(None, "Incorrect argument on command line:\n   -"
                                  "Correct usage: uv run python pac-man.py "
                                  "config.json")
    return known
