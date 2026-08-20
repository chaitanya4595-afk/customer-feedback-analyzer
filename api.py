"""Convenient FastAPI entry point for local development."""

from pathlib import Path
import sys

# Keep this entry point runnable from a source checkout before installation.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from project_feedback_analyzer.api import app

__all__ = ["app"]
