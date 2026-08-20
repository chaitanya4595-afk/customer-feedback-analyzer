"""Gemini integration for structured customer-review analysis."""

from google import genai
from google.genai import types
from pydantic import ValidationError

from project_feedback_analyzer.models import Analysis


class AnalysisProviderError(RuntimeError):
    """Raised when Gemini cannot provide a valid analysis."""


class GeminiAnalyzer:
    """Analyze customer reviews with Google Gemini."""

    def __init__(self, api_key: str, model: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def analyze(self, review_text: str) -> Analysis:
        """Return a validated sentiment, score, and theme for one review."""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=(
                    "Analyze this customer review.\n"
                    "label must be 'positive', 'negative', or 'neutral'.\n"
                    "score must be a number from 1 (very bad) to 5 (very good).\n"
                    "theme must be ONE lowercase word for the main topic "
                    "(for example: delivery, taste, price, service, quality).\n"
                    f"Review: {review_text}"
                ),
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=Analysis,
                ),
            )
        except Exception as exc:
            raise AnalysisProviderError("Gemini could not analyze the review.") from exc

        if response.parsed is None:
            raise AnalysisProviderError("Gemini returned an empty response.")

        try:
            return Analysis.model_validate(response.parsed)
        except ValidationError as exc:
            raise AnalysisProviderError("Gemini returned an invalid response.") from exc
