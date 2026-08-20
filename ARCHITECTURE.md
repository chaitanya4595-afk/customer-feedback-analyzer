# Architecture

## Overview

Customer Feedback Analyzer uses a small client-server design. Streamlit owns
the user experience, FastAPI exposes the analysis contract, Gemini performs the
language analysis, and SQLite stores results the user chooses to save.

```text
Customer
   │
   │ pastes reviews
   ▼
Streamlit dashboard (app.py)
   │
   │ one POST /analyze request per review
   ▼
FastAPI application (project_feedback_analyzer.api)
   │
   │ validated review text
   ▼
Gemini service (project_feedback_analyzer.service)
   │
   │ structured Analysis response
   ▼
Streamlit summary and results table
   │
   │ explicit save action
   ▼
SQLite database (project_feedback_analyzer.database)
```

## Components

### Streamlit dashboard

The root `app.py` is the UI entry point. It parses non-empty lines, calls the
configured FastAPI URL with an HTTP timeout, validates responses, and reports
request failures per review. Successful analyses are passed to pure analytics
functions for aggregation and can be saved to SQLite.

### FastAPI service

The root `api.py` is a thin entry point that exposes the package-level FastAPI
application. `project_feedback_analyzer.api` validates requests, constructs the
Gemini service from environment settings, and maps configuration or provider
failures to suitable HTTP responses.

### Validation models

`project_feedback_analyzer.models` defines the API contract with Pydantic.
Review text must be non-empty, sentiment is restricted to the supported three
labels, scores range from 1 to 5, and themes must be one lowercase word.

### Gemini service

`project_feedback_analyzer.service` contains the only direct Gemini SDK usage.
It requests structured JSON, validates the parsed response, and converts empty,
invalid, or failed provider responses into an application-specific exception.

### Analytics

`project_feedback_analyzer.analytics` contains deterministic summary logic.
Failed reviews are excluded from average score, positive percentage, and theme
calculations. Keeping this logic independent from Streamlit makes it easy to
test.

### SQLite persistence

`project_feedback_analyzer.database` initializes and accesses the existing
`feedback` table through context-managed connections. Its schema remains:

```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    review TEXT,
    label TEXT,
    score INTEGER,
    theme TEXT
);
```

Failed review results are never inserted. The database path is configurable,
which also allows tests to use isolated temporary databases.

## Configuration

Configuration is loaded by `project_feedback_analyzer.config` from environment
variables and an optional `.env` file. This keeps secrets and machine-specific
paths outside source code. See `.env.example` for all supported settings.

## Failure handling

- Invalid review requests are rejected by FastAPI with HTTP 422.
- Missing credentials produce HTTP 503 with a configuration message.
- Gemini failures and invalid or empty model responses produce HTTP 502.
- Streamlit handles timeouts, connection failures, HTTP errors, and invalid API
  payloads without stopping the rest of the batch.
- Failed rows remain visible for transparency but are excluded from metrics and
  database saves.

## Testing boundary

The FastAPI application accepts an injected analyzer function. API tests use
this boundary to simulate successful and failed Gemini behavior without making
network requests or consuming API credits. Database tests use a temporary
SQLite file, and analytics tests exercise pure functions.
