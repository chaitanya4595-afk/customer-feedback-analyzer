from project_feedback_analyzer.analytics import calculate_summary


def test_summary_has_one_clear_top_theme_and_excludes_failures() -> None:
    results = [
        {"label": "positive", "score": 5, "theme": "service"},
        {"label": "neutral", "score": 3, "theme": "service"},
        {"label": "positive", "score": 4, "theme": "price"},
        {"label": "error", "score": 0, "theme": "error"},
    ]

    summary = calculate_summary(results)

    assert summary.total == 4
    assert summary.succeeded == 3
    assert summary.failed == 1
    assert summary.average_score == 4.0
    assert summary.positive_percentage == 67
    assert summary.top_themes == ("service",)


def test_summary_returns_all_themes_tied_for_highest_count() -> None:
    results = [
        {"label": "positive", "score": 5, "theme": "service"},
        {"label": "neutral", "score": 3, "theme": "delivery"},
        {"label": "positive", "score": 4, "theme": "quality"},
    ]

    summary = calculate_summary(results)

    assert summary.top_themes == ("service", "delivery", "quality")


def test_summary_handles_no_valid_themes() -> None:
    summary = calculate_summary(
        [{"label": "error", "score": 0, "theme": "error"}]
    )

    assert summary.succeeded == 0
    assert summary.failed == 1
    assert summary.average_score is None
    assert summary.positive_percentage is None
    assert summary.top_themes == ()
