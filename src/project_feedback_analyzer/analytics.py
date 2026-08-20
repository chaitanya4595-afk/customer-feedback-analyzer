"""Pure functions for calculating dashboard summary metrics."""

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Mapping, Any


@dataclass(frozen=True)
class Summary:
    """Aggregate metrics for a batch of review results."""

    total: int
    succeeded: int
    failed: int
    average_score: float | None
    positive_percentage: float | None
    top_themes: tuple[str, ...]


def calculate_summary(results: Iterable[Mapping[str, Any]]) -> Summary:
    """Calculate metrics using successful analyses only."""
    result_list = list(results)
    successful = [result for result in result_list if result.get("label") != "error"]
    failed = len(result_list) - len(successful)

    if not successful:
        return Summary(
            total=len(result_list),
            succeeded=0,
            failed=failed,
            average_score=None,
            positive_percentage=None,
            top_themes=(),
        )

    scores = [int(result["score"]) for result in successful]
    positive_count = sum(result["label"] == "positive" for result in successful)
    themes = [
        str(result["theme"])
        for result in successful
        if result.get("theme") and result.get("theme") != "error"
    ]
    theme_counts = Counter(themes)
    highest_count = max(theme_counts.values(), default=0)
    top_themes = tuple(
        theme for theme, count in theme_counts.items() if count == highest_count
    )

    return Summary(
        total=len(result_list),
        succeeded=len(successful),
        failed=failed,
        average_score=round(sum(scores) / len(scores), 1),
        positive_percentage=round(positive_count / len(successful) * 100),
        top_themes=top_themes,
    )
