# Built-in modules
from pathlib import Path

# Installed modules
import pytest

# Local modules
from src.backend import Highscores
from src.exceptions import PacManError


@pytest.fixture
def highscores(tmp_path: Path) -> Highscores:
    """Empty table backed by a temp file, fresh per test."""
    return Highscores(tmp_path / "scores.json")


class TestInsert:
    """Validation of ``Highscores.insert``."""

    @pytest.mark.parametrize("name", ["", " Bad", "Again!!",
                                      "THISISTOLONGFORANAME"])
    def test_invalid_name(self, highscores: Highscores, name: str) -> None:
        assert not highscores.insert(name, 10)
        assert highscores.table == []

    def test_valid_insert(self, highscores: Highscores) -> None:
        assert highscores.insert("PacMaster", 50)
        assert len(highscores.table) == 1
        entry = highscores.table[0]
        assert entry.name == "PacMaster"
        assert entry.score == 50

    def test_negative_score(self, highscores: Highscores) -> None:
        assert not highscores.insert("Wrong", -50)
        assert highscores.table == []

    def test_keeps_top_ten_sorted(self, highscores: Highscores) -> None:
        for score in range(15):
            highscores.insert(f"P{score}", score)
        assert len(highscores.table) == 10
        scores = [entry.score for entry in highscores.table]
        assert scores == sorted(scores, reverse=True)


class TestLoadSave:
    """Validation of ``Highscores.save and Highscores.load``."""

    def test_round_trip(self, highscores: Highscores) -> None:
        highscores.insert("Daniel", 42)
        highscores.insert("Martin", 67)
        highscores.save()
        new_table = Highscores(highscores.path)
        new_table.load()
        assert new_table.table == highscores.table

    def test_missing_file(self, highscores: Highscores) -> None:
        highscores.load()
        assert highscores.table == []

    @pytest.mark.parametrize("content", [
        "{bad",
        "42",
        "null",
        '[{"name": "Bad!", "score": 1}]',
        '[{"name": "Al"}]'])
    def test_invalid_file(self, highscores: Highscores, content: str) -> None:
        highscores.path.write_text(content)
        with pytest.raises(PacManError):
            highscores.load()
        assert highscores.table == []

    def test_failed_load_clears_table(self, highscores: Highscores) -> None:
        highscores.insert("MrPac", 100)
        highscores.save()
        highscores.path.write_text("{bad")
        with pytest.raises(PacManError):
            highscores.load()
        assert highscores.table == []

    def test_save_failure(self, tmp_path: Path) -> None:
        highscores = Highscores(tmp_path)
        highscores.insert("Pac", 10)
        with pytest.raises(PacManError):
            highscores.save()

