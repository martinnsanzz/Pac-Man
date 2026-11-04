# Built-in modules
from argparse import ArgumentError

# Installed modules
import pytest

# Local modules
from src.parsing import load_arguments


def test_extra_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["src", "config.json", "extra"])
    with pytest.raises(ArgumentError,
                       match="Incorrect argument on command line"):
        load_arguments()


def test_empty_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["src"])
    with pytest.raises(ArgumentError, match="Missing config file in CLI."):
        load_arguments()


def test_incorrect_config_format(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["src", "config.txt"])
    with pytest.raises(ArgumentError, match="isn't a valid json file"):
        load_arguments()


def test_different_config_name(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["src", "random.json"])
    args = load_arguments()
    assert args.file == "random.json"


def test_valid_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["src", "config.json"])
    args = load_arguments()
    assert args.file == "config.json"
