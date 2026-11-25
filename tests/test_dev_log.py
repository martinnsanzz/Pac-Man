# Installed modules
import pytest

# Local modules
from src.backend import DevLog, LogKind


@pytest.fixture
def log() -> DevLog:
    """Fresh DevLog with no entries and an empty input line."""
    return DevLog()


def type_text(log: DevLog, text: str) -> None:
    """Feed each character of text into the input line."""
    for char in text:
        log.add_char(char)


class TestAdd:
    """Validation of ``DevLog.add``."""

    def test_add_one(self, log: DevLog) -> None:
        log.add("hello", LogKind.INFO)
        assert len(log.entries) == 1
        assert log.entries[-1].text == "hello"
        assert log.entries[-1].kind is LogKind.INFO

    def test_keeps_order(self, log: DevLog) -> None:
        log.add("first", LogKind.INFO)
        log.add("second", LogKind.WARNING)
        assert [entry.text for entry in log.entries] == ["first", "second"]

    def test_drops_oldest_past_max(self, log: DevLog) -> None:
        for i in range(DevLog.MAX_ENTRIES + 1):
            log.add(f"msg {i}", LogKind.MESSAGE)
        assert len(log.entries) == DevLog.MAX_ENTRIES
        assert log.entries[0].text == "msg 1"
        assert log.entries[-1].text == f"msg {DevLog.MAX_ENTRIES}"


class TestInput:
    """Validation of ``DevLog.add_char`` and ``DevLog.backspace``."""

    def test_add_char_keeps_order_and_case(self, log: DevLog) -> None:
        type_text(log, "aB/1 x")
        assert log.text == "aB/1 x"

    # \x1b -> escape // \x08 -> backspace
    @pytest.mark.parametrize("char", ["", "\r", "\n", "\t", "\x08", "\x1b"])
    def test_ignores_non_printable(self, log: DevLog, char: str) -> None:
        log.add_char(char)
        assert log.text == ""

    def test_backspace(self, log: DevLog) -> None:
        type_text(log, "abc")
        log.backspace()
        assert log.text == "ab"

    def test_backspace_on_empty(self, log: DevLog) -> None:
        log.backspace()
        assert log.text == ""


class TestSubmit:
    """Validation of ``DevLog.submit``."""

    def test_returns_text_and_clears(self, log: DevLog) -> None:
        type_text(log, "/IMMORTAL")
        assert log.submit() == "/IMMORTAL"
        assert log.text == ""

    def test_strips_spaces(self, log: DevLog) -> None:
        type_text(log, "  /IMMORTAL  ")
        assert log.submit() == "/IMMORTAL"

    def test_empty_input(self, log: DevLog) -> None:
        assert log.submit() == ""

    def test_does_not_add_entry(self, log: DevLog) -> None:
        type_text(log, "hello")
        log.submit()
        assert log.entries == []
