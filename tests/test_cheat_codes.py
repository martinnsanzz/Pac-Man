# Installed modules
import pytest

# Local modules
from src.backend import Cheat, CheatCodes
from src.backend.cheat_codes import MAX_LENGTH


@pytest.fixture
def cheats() -> CheatCodes:
    """Fresh cheat input with nothing typed and no active cheats."""
    return CheatCodes()


def type_code(cheats: CheatCodes, text: str) -> Cheat | None:
    """Type every character of text, then submit it."""
    for char in text:
        cheats.add_char(char)
    return cheats.submit()


class TestInput:
    """Validation of ``CheatCodes.add_char`` and ``CheatCodes.backspace``."""

    def test_uppercase(self, cheats: CheatCodes) -> None:
        for char in "abc":
            cheats.add_char(char)
        assert cheats.text == "ABC"

    @pytest.mark.parametrize("char", ["0", "!", " ", "é", "-"])
    def test_ignores_invalid_chars(self, cheats: CheatCodes,
                                   char: str) -> None:
        cheats.add_char(char)
        assert cheats.text == ""

    def text_max_length(self, cheats: CheatCodes) -> None:
        for char in "A" * (MAX_LENGTH + 3):
            cheats.add_char(char)
        assert len(cheats.text) == MAX_LENGTH

    def test_backspace(self, cheats: CheatCodes) -> None:
        for char in "ABC":
            cheats.add_char(char)
        cheats.backspace()
        assert cheats.text == "AB"

    def test_backspace_empty(self, cheats: CheatCodes) -> None:
        cheats.backspace()
        assert cheats.text == ""


class TestSubmit:
    """Validation of ``CheatCodes.submit``."""

    @pytest.mark.parametrize("cheat", list(Cheat))
    def test_valid_code(self, cheats: CheatCodes, cheat: Cheat) -> None:
        assert type_code(cheats, cheat.value.lower()) is cheat

    @pytest.mark.parametrize("text", ["", "BANANA", "IMMORTA", "XIMMORTAL"])
    def test_invalid_code(self, cheats: CheatCodes, text: str) -> None:
        assert type_code(cheats, text) is None

    def test_clears_text_on_success(self, cheats: CheatCodes) -> None:
        type_code(cheats, "IMMORTAL")
        assert cheats.text == ""

    def test_clears_text_on_failure(self, cheats: CheatCodes) -> None:
        type_code(cheats, "BANANA")
        assert cheats.text == ""


class TestToggles:
    """Validation of toggle, one-shot and NOCHEATS behaviour."""

    def test_toggle_on(self, cheats: CheatCodes) -> None:
        type_code(cheats, "IMMORTAL")
        assert cheats.is_active(Cheat.IMMORTAL)

    def test_toggle_off(self, cheats: CheatCodes) -> None:
        type_code(cheats, "IMMORTAL")
        type_code(cheats, "IMMORTAL")
        assert not cheats.is_active(Cheat.IMMORTAL)

    @pytest.mark.parametrize("cheat",
                             [c for c in Cheat if c in CheatCodes.ONE_SHOTS])
    def test_one_shots_never_active(self, cheats: CheatCodes,
                                    cheat: Cheat) -> None:
        type_code(cheats, cheat.value)
        assert cheats.active == set()

    def test_nocheats_clears_all(self, cheats: CheatCodes) -> None:
        type_code(cheats, "IMMORTAL")
        type_code(cheats, "ZOOMZOOM")
        type_code(cheats, "NOCHEATS")
        assert cheats.active == set()
