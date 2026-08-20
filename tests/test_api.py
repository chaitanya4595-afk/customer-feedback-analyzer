from fastapi.testclient import TestClient
from pathlib import Path

from project_feedback_analyzer.api import create_app
from project_feedback_analyzer.config import Settings
from project_feedback_analyzer.models import Analysis
from project_feedback_analyzer.service import AnalysisProviderError


def test_analyze_returns_mocked_result() -> None:
    app = create_app(
        analyzer=lambda text: Analysis(label="positive", score=5, theme="service")
    )
    client = TestClient(app)

    response = client.post("/analyze", json={"text": "Excellent service"})

    assert response.status_code == 200
    assert response.json() == {"label": "positive", "score": 5, "theme": "service"}


def test_analyze_rejects_empty_review() -> None:
    app = create_app(analyzer=lambda text: Analysis(label="neutral", score=3, theme="value"))
    client = TestClient(app)

    response = client.post("/analyze", json={"text": "   "})

    assert response.status_code == 422


def test_analyze_handles_provider_failure() -> None:
    def failing_analyzer(text: str) -> Analysis:
        raise AnalysisProviderError("Gemini could not analyze the review.")

    client = TestClient(create_app(analyzer=failing_analyzer))
    response = client.post("/analyze", json={"text": "A valid review"})

    assert response.status_code == 502
    assert response.json()["detail"] == "Gemini could not analyze the review."


def test_analyze_reports_missing_api_key() -> None:
    settings = Settings(
        gemini_api_key=None,
        gemini_model="test-model",
        api_url="http://test/analyze",
        http_timeout=1,
        database_path=Path("feedback.db"),
    )
    client = TestClient(create_app(settings=settings))

    response = client.post("/analyze", json={"text": "A valid review"})

    assert response.status_code == 503
    assert "API key is missing" in response.json()["detail"]
