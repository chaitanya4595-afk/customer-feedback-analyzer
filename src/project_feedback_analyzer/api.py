"""FastAPI application for customer-review analysis."""

from collections.abc import Callable

from fastapi import FastAPI, HTTPException, status

from project_feedback_analyzer.config import (
    ConfigurationError,
    Settings,
    get_settings,
    require_gemini_api_key,
)
from project_feedback_analyzer.models import Analysis, ReviewRequest
from project_feedback_analyzer.service import AnalysisProviderError, GeminiAnalyzer

Analyzer = Callable[[str], Analysis]


def create_app(
    analyzer: Analyzer | None = None,
    settings: Settings | None = None,
) -> FastAPI:
    """Create the API, optionally injecting an analyzer for tests."""
    application = FastAPI(
        title="Customer Feedback Analyzer API",
        description="Convert customer reviews into sentiment, score, and theme data.",
        version="0.1.0",
    )

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @application.post("/analyze", response_model=Analysis)
    def analyze_review(review: ReviewRequest) -> Analysis:
        try:
            if analyzer is not None:
                return analyzer(review.text)

            runtime_settings = settings or get_settings()
            api_key = require_gemini_api_key(runtime_settings)
            service = GeminiAnalyzer(api_key, runtime_settings.gemini_model)
            return service.analyze(review.text)
        except ConfigurationError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc),
            ) from exc
        except AnalysisProviderError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(exc),
            ) from exc

    return application


app = create_app()
