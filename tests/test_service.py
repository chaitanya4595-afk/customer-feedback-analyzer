from types import SimpleNamespace

import pytest

from project_feedback_analyzer.service import AnalysisProviderError, GeminiAnalyzer


class FakeModels:
    def __init__(self, parsed) -> None:
        self.parsed = parsed

    def generate_content(self, **kwargs):
        return SimpleNamespace(parsed=self.parsed)


def analyzer_with_response(parsed) -> GeminiAnalyzer:
    analyzer = GeminiAnalyzer.__new__(GeminiAnalyzer)
    analyzer.client = SimpleNamespace(models=FakeModels(parsed))
    analyzer.model = "mock-model"
    return analyzer


def test_gemini_analyzer_validates_mocked_response() -> None:
    result = analyzer_with_response(
        {"label": "negative", "score": 2, "theme": "service"}
    ).analyze("Slow customer support")

    assert result.label == "negative"
    assert result.score == 2
    assert result.theme == "service"


def test_gemini_analyzer_rejects_empty_response() -> None:
    with pytest.raises(AnalysisProviderError, match="empty response"):
        analyzer_with_response(None).analyze("A valid review")
