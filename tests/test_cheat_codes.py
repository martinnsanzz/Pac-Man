# Installed modules
import pytest

# Local modules
from src.backend import Cheat, CheatCodes


@pytest.fixture
def cheats() -> CheatCodes:
    """Fresh cheat input with nothing typed and no active cheats."""
    return CheatCodes()


class TestSubmit:
    """Validation of ``CheatCodes.submit``."""

    @pytest.mark.parametrize("cheat", list(Cheat))
    @pytest.mark.parametrize("upper", [True, False])
    def test_valid_code(self, cheats: CheatCodes, cheat: Cheat,
                        upper: bool) -> None:
        code = cheat.value if upper else cheat.value.lower()
        assert cheats.submit("/" + code) is cheat

    @pytest.mark.parametrize("text", ["", "BANANA", "IMMORTA", "XIMMORTAL"])
    def test_invalid_code(self, cheats: CheatCodes, text: str) -> None:
        assert cheats.submit("/" + text) is None


class TestToggles:
    """Validation of toggle, one-shot and NOCHEATS behaviour."""

    def test_toggle_on(self, cheats: CheatCodes) -> None:
        cheats.submit("/" + "IMMORTAL")
        assert cheats.is_active(Cheat.IMMORTAL)

    def test_toggle_off(self, cheats: CheatCodes) -> None:
        cheats.submit("/" + "IMMORTAL")
        cheats.submit("/" + "IMMORTAL")
        assert not cheats.is_active(Cheat.IMMORTAL)

    @pytest.mark.parametrize("cheat",
                             [c for c in Cheat if c in CheatCodes.ONE_SHOTS])
    def test_one_shots_never_active(self, cheats: CheatCodes,
                                    cheat: Cheat) -> None:
        cheats.submit("/" + cheat.value)
        assert cheats.active == set()

    def test_nocheats_clears_all(self, cheats: CheatCodes) -> None:
        cheats.submit("/" + "IMMORTAL")
        cheats.submit("/" + "ZOOMZOOM")
        cheats.submit("/" + "NOCHEATS")
        assert cheats.active == set()
