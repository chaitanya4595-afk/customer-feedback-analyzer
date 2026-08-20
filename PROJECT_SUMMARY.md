# Project Summary

## Two-sentence portfolio description

Customer Feedback Analyzer is an end-to-end applied AI application that turns
unstructured customer reviews into validated sentiment labels, satisfaction
scores, and topic themes. It combines a Streamlit dashboard, a FastAPI service,
Google Gemini structured output, tested analytics logic, and SQLite persistence
to make qualitative feedback easier to review.

## Resume bullets

- Built an end-to-end customer feedback analysis application using Python,
  Streamlit, FastAPI, Google Gemini, Pydantic, and SQLite.
- Designed a validated REST API that converts unstructured reviews into
  sentiment, 1–5 scores, and one-word themes while handling missing credentials,
  invalid input, and AI provider failures.
- Extracted testable analytics and persistence layers, added mocked API tests
  that avoid live AI calls, and excluded failed analyses from business summary
  metrics and stored results.

## 30-second interview explanation

I built this project to demonstrate how an applied AI feature can be turned
into a usable analytics workflow rather than left as a standalone model call.
A business user pastes customer reviews into Streamlit, a FastAPI backend asks
Gemini for a constrained sentiment, score, and theme response, and the dashboard
summarizes only successful results. Users can save those results to SQLite and
view their history. I separated configuration, validation, AI integration,
analytics, and persistence so each part is understandable and testable.

## Technical challenges solved

- Converting variable natural-language model output into a strict Pydantic
  response contract.
- Separating Streamlit presentation logic from reusable analytics and database
  code.
- Handling partial batch failures without discarding successful review results.
- Ensuring failed analyses do not distort metrics or enter the database.
- Making credentials, model selection, endpoint location, timeouts, and storage
  paths environment-configurable.
- Testing API behavior through dependency injection without sending real Gemini
  requests.
- Preserving compatibility with an existing SQLite table while improving
  connection handling.

## Potential business applications

- Summarizing product or service feedback collected from surveys.
- Triaging reviews that may need customer-support follow-up.
- Identifying frequently discussed themes across small feedback batches.
- Creating a structured input for exploratory customer-experience analysis.
- Prototyping an internal voice-of-customer dashboard before adopting a larger
  analytics platform.

The current project is a local portfolio application, not a production-scale
customer intelligence system. Its outputs should be reviewed by a person before
they are used for consequential business decisions.
