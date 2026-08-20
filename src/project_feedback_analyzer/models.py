"""Validated request and response models shared across the application."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ReviewRequest(BaseModel):
    """A single customer review submitted for analysis."""

    text: str = Field(min_length=1, max_length=10_000)

    @field_validator("text")
    @classmethod
    def review_must_contain_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Review text cannot be empty.")
        return cleaned


class Analysis(BaseModel):
    """Structured sentiment analysis returned by Gemini and the API."""

    label: Literal["positive", "negative", "neutral"]
    score: int = Field(ge=1, le=5)
    theme: str = Field(min_length=1, max_length=50, pattern=r"^[a-z]+$")
