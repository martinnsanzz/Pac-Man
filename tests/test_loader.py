# Built-in modules
from pathlib import Path
from json import dumps

# Installed modules
import pytest

# Local modules
from src.parsing import load_json
from src.exceptions import PacManError

PYTHON_COMMENT = "# Python Comment\n"
CPP_COMMENT = "// CPP Comment\n"
C_COMMENT = "/* C Comment */\n"
MULTI_LINE_COMMENT = "/* Hello\n Hello2\n Hello3\n */\n"
MULTIPLE_SINGLE_LINE_COMMENTS = PYTHON_COMMENT + CPP_COMMENT + C_COMMENT


def test_single_line_comments(tmp_path: Path) -> None:
    tmp_data = dumps({"Test": 5})

    f = tmp_path / "config.json"
    f.write_text(MULTIPLE_SINGLE_LINE_COMMENTS + tmp_data)

    result = load_json(f)
    assert result["Test"] == 5


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(PacManError, match="No such file"):
        load_json(tmp_path / "nope.json")


def test_no_permissions(tmp_path: Path) -> None:
    f = tmp_path / "config.json"
    f.write_text("data")
    f.chmod(0o000)
    with pytest.raises(PacManError, match="Permission denied"):
        load_json(f)


def test_empty_file(tmp_path: Path) -> None:
    f = tmp_path / "config.json"
    f.write_text("")
    with pytest.raises(PacManError, match="config.json is empty"):
        load_json(f)


def test_only_spaces(tmp_path: Path) -> None:
    f = tmp_path / "config.json"
    f.write_text("   \n\n\t\t   ")
    with pytest.raises(PacManError, match="config.json is empty"):
        load_json(f)


def test_only_comments(tmp_path: Path) -> None:
    f = tmp_path / "config.json"
    f.write_text(MULTIPLE_SINGLE_LINE_COMMENTS)
    with pytest.raises(PacManError, match="config.json is empty"):
        load_json(f)


def test_invalid_encoder(tmp_path: Path) -> None:
    f = tmp_path / "config.json"
    f.write_bytes(b"\xff\xfe\x00\x80")
    with pytest.raises(PacManError, match="Decode error found"):
        load_json(f)


def test_multiline_comment(tmp_path: Path) -> None:
    tmp_data = dumps({"Test": 5})

    f = tmp_path / "config.json"
    f.write_text(MULTI_LINE_COMMENT + tmp_data + "\n" +
                 MULTIPLE_SINGLE_LINE_COMMENTS)

    result = load_json(f)
    assert result["Test"] == 5


def test_valid_config(tmp_path: Path) -> None:
    tmp_data = dumps({"Test": 5})

    f = tmp_path / "config.json"
    f.write_text(tmp_data)

    result = load_json(f)
    assert result["Test"] == 5
