from project_feedback_analyzer.database import init_db, load_history, save_results


def test_save_and_load_results_uses_existing_schema(tmp_path) -> None:
    database_path = tmp_path / "test_feedback.db"
    init_db(database_path)

    saved = save_results(
        [
            {
                "review": "Fast delivery",
                "label": "positive",
                "score": 5,
                "theme": "delivery",
            },
            {
                "review": "Backend unavailable",
                "label": "error",
                "score": 0,
                "theme": "error",
            },
        ],
        database_path,
    )

    assert saved == 1
    assert load_history(database_path) == [
        ("Fast delivery", "positive", 5, "delivery")
    ]
