# Built-in
from argparse import ArgumentParser, ArgumentError, Namespace


def json_file(file: str) -> str:
    """Checks if file name ends with '.json' extension"""
    if not file.lower().endswith(".json"):
        raise TypeError(f"'{file}' isn't a valid json file.")
    return file


def load_arguments() -> Namespace:
    """Parse and validate the command-line arguments.

    Expect exactly one positional argument: the path to a ``.json``
    configuration file. The path is checked with ``json_file``.

    Returns:
        The parsed arguments, with the configuration path in ``file``.

    Raises:
        ArgumentError: If the configuration file is missing, fails the
            ``json_file`` check, or if any unrecognized arguments are
            present on the command line.
    """
    parser = ArgumentParser(description="Read a file from CLI",
                            exit_on_error=False)

    parser.add_argument("file", nargs="?")

    known, unknown = parser.parse_known_args()
    if known.file is None:
        raise ArgumentError(None, "Missing config file in CLI.")

    try:
        json_file(known.file)
    except TypeError as e:
        raise ArgumentError(None, str(e)) from e

    if unknown:
        raise ArgumentError(None, "Incorrect argument on command line:\n   -"
                                  "Correct usage: uv run python pac-man.py "
                                  "config.json")
    return known
