# Built-in modules
from typing import Any
from json import loads, JSONDecodeError

# Local modules
from ..exceptions import PacManError


def is_comment(line: str) -> bool:
    if line.startswith("#") or line.startswith("//"):
        return True
    elif line.startswith("/*") and line.endswith("*/"):
        return True
    return False

def load_json(file: str) -> dict[str, Any]:
    data: dict[str, Any] = dict()
    config_raw: list[str] = []

    try:
        with open(file, encoding="utf-8") as f:
            content = f.readlines()

        clean = [line.strip() for line in content if line.strip()]

        for line in clean:
            if not is_comment(line):
                config_raw.append(line + "\n")
        data = loads("".join(config_raw))
    except OSError as e:
        raise PacManError(f"{e.strerror} '{file}'") from e
    except UnicodeDecodeError as e:
        raise PacManError(f"Decode error found. File must be 'utf-8'")
    except JSONDecodeError as e:
        raise PacManError(f"Wrong JSON format in {file}: {e}") from e
    return data
