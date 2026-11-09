# Built-in modules
from typing import Any, cast
from json import loads, JSONDecodeError
from pathlib import Path

# Local modules
from ..exceptions import PacManError


def is_comment(line: str) -> bool:
    """Check whether a line is a single-line comment.

    Recognize Python-style (``#``) comments, C++-style (``//``) comments,
    and C-style block comments (``/* ... */``) that open and close on the
    same line.

    Returns:
        True if the line starts with ``#`` or ``//``, or starts with
        ``/*`` and ends with ``*/``. False otherwise.
    """
    if line.startswith("#") or line.startswith("//"):
        return True
    elif line.startswith("/*") and line.endswith("*/"):
        return True
    return False


def extract_data(lines: list[str]) -> list[str]:
    """Remove comments from configuration lines.

    Drop single-line comments (see ``is_comment``) and multi-line
    ``/* ... */`` blocks, including the lines that open and close a block.
    Each remaining line is returned with a trailing newline appended.

    Args:
        lines: Source lines of the configuration file.

    Returns:
        The lines that are not comments, each terminated with ``"\\n"``.

    Raises:
        PacManError: If a ``/*`` block is opened and never closed.
    """
    raw = []
    in_comment = False

    for line in lines:
        if is_comment(line):
            continue
        if line.startswith("/*"):
            in_comment = True
        elif line.endswith("*/"):
            in_comment = False
            continue

        if not in_comment:
            raw.append(line + "\n")

    if in_comment:
        raise PacManError("Found open multi-line comment /* */ on config file")
    return raw


def load_json(file: Path) -> dict[str, Any]:
    """Load and parse a JSON file into a dictionary.

    Read the file as UTF-8, discard blank lines and surrounding whitespace,
    pass the remaining lines through ``extract_data``, and parse the joined
    result as JSON.

    Args:
        file: Path to the JSON file to load.

    Returns:
        The parsed JSON content.

    Raises:
        PacManError: If the file cannot be opened or read, is not valid
            UTF-8, or does not contain valid JSON.
    """
    try:
        with open(file, encoding="utf-8") as f:
            content = f.readlines()
        clean = [line.strip() for line in content if line.strip()]

        raw_data = extract_data(clean)

        if not raw_data:
            raise PacManError(f"{file} is empty.")

        parsed = loads("".join(raw_data))
    except OSError as e:
        raise PacManError(f"{e.strerror} '{file}'") from e
    except UnicodeDecodeError as e:
        raise PacManError(f"Decode error found on '{file}'.\n"
                          "File must be 'utf-8'") from e
    except JSONDecodeError as e:
        raise PacManError(f"Wrong JSON format in {file}: {e}") from e
    return cast(dict[str, Any], parsed)
