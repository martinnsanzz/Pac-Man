# Built-in modules
import json
from pathlib import Path

# Installed modules
import pytest

# Local modules
from src.backend import Highscores
from src.exceptions import HighScoreError


@pytest.fixture
def highscores(tmp_path: Path) -> Highscores:
    """Empty table backed by a file in a ``data/`` folder that doesn't exist
    yet, fresh per test."""
    return Highscores(tmp_path / "data" / "scores.json")


def write_raw(path: Path, content: str) -> None:
    """Write `content` to `path`, creating its folder first."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


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


class TestQueries:
    """Validation of ``is_highscore`` and ``get_high_score``."""

    def test_high_score_of_empty_table(self, highscores: Highscores) -> None:
        assert highscores.get_high_score() == 0

    def test_high_score_is_the_best(self, highscores: Highscores) -> None:
        highscores.insert("Low", 10)
        highscores.insert("Top", 90)
        highscores.insert("Mid", 50)
        assert highscores.get_high_score() == 90

    def test_is_highscore_while_not_full(self,
                                         highscores: Highscores) -> None:
        highscores.insert("Pac", 100)
        assert highscores.is_highscore(1)

    def test_is_highscore_when_full(self, highscores: Highscores) -> None:
        for score in range(1, 11):
            highscores.insert(f"P{score}", score)
        assert not highscores.is_highscore(1)   # ties the lowest entry
        assert highscores.is_highscore(2)


class TestLoadSave:
    """Validation of ``Highscores.save and Highscores.load``."""

    def test_round_trip(self, highscores: Highscores) -> None:
        highscores.insert("Daniel", 42)
        highscores.insert("Martin", 67)
        highscores.save()
        new_table = Highscores(highscores.path)
        new_table.load()
        assert new_table.table == highscores.table

    def test_load_sorts_and_trims(self, highscores: Highscores) -> None:
        entries = [{"name": f"P{score}", "score": score}
                   for score in (5, 12, 1, 9, 3, 11, 7, 2, 10, 4, 8, 6)]
        write_raw(highscores.path, json.dumps(entries))
        highscores.load()
        scores = [entry.score for entry in highscores.table]
        assert scores == [12, 11, 10, 9, 8, 7, 6, 5, 4, 3]

    def test_save_creates_data_folder(self, highscores: Highscores) -> None:
        assert not highscores.path.parent.exists()
        highscores.insert("Pac", 10)
        highscores.save()
        assert highscores.path.is_file()

    def test_save_one_entry_per_line(self, highscores: Highscores) -> None:
        highscores.insert("Daniel", 42)
        highscores.insert("Martin", 67)
        highscores.save()
        lines = highscores.path.read_text().splitlines()
        assert lines[0] == "["
        assert lines[-1] == "]"
        assert len(lines) == len(highscores.table) + 2

    def test_save_empty_table(self, highscores: Highscores) -> None:
        highscores.save()
        assert highscores.path.read_text() == "[]\n"

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
        write_raw(highscores.path, content)
        with pytest.raises(HighScoreError):
            highscores.load()
        assert highscores.table == []

    def test_failed_load_clears_table(self, highscores: Highscores) -> None:
        highscores.insert("MrPac", 100)
        highscores.save()
        highscores.path.write_text("{bad")
        with pytest.raises(HighScoreError):
            highscores.load()
        assert highscores.table == []

    def test_save_failure_path_is_folder(self, tmp_path: Path) -> None:
        highscores = Highscores(tmp_path)
        highscores.insert("Pac", 10)
        with pytest.raises(HighScoreError):
            highscores.save()

    def test_save_failure_parent_is_file(self, tmp_path: Path) -> None:
        blocker = tmp_path / "data"
        blocker.write_text("not a folder")
        highscores = Highscores(blocker / "scores.json")
        highscores.insert("Pac", 10)
        with pytest.raises(HighScoreError):
            highscores.save()
