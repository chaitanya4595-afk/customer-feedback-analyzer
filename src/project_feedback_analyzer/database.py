"""SQLite persistence for analyzed customer reviews."""

import sqlite3
from pathlib import Path
from typing import Iterable, Mapping, Any

from project_feedback_analyzer.config import get_settings


def _database_path(database_path: str | Path | None = None) -> Path:
    return Path(database_path) if database_path is not None else get_settings().database_path


def init_db(database_path: str | Path | None = None) -> None:
    """Create the existing feedback table if it does not already exist."""
    path = _database_path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY,
                review TEXT,
                label TEXT,
                score INTEGER,
                theme TEXT
            )
            """
        )


def save_results(
    results: Iterable[Mapping[str, Any]],
    database_path: str | Path | None = None,
) -> int:
    """Save successful results and return the number of inserted rows."""
    successful = [result for result in results if result.get("label") != "error"]
    if not successful:
        return 0

    path = _database_path(database_path)
    with sqlite3.connect(path) as connection:
        connection.executemany(
            "INSERT INTO feedback (review, label, score, theme) VALUES (?, ?, ?, ?)",
            [
                (result["review"], result["label"], result["score"], result["theme"])
                for result in successful
            ],
        )
    return len(successful)


def load_history(database_path: str | Path | None = None) -> list[tuple]:
    """Return all saved reviews in insertion order."""
    path = _database_path(database_path)
    with sqlite3.connect(path) as connection:
        return connection.execute(
            "SELECT review, label, score, theme FROM feedback ORDER BY id"
        ).fetchall()
