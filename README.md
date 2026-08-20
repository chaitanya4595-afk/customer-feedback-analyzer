# Customer Feedback Analyzer

A small AI-powered dashboard that turns customer reviews into structured,
business-friendly insights. Each review is classified by sentiment, assigned a
score from 1 to 5, and grouped under a one-word theme such as `delivery`,
`price`, or `service`.

The project combines:

- **Streamlit** for the interactive dashboard
- **FastAPI** for the analysis API
- **Google Gemini** for structured review analysis
- **SQLite** for persistent review history

## How it works

1. A user pastes one or more reviews into the Streamlit dashboard.
2. The dashboard sends each review to the FastAPI `POST /analyze` endpoint.
3. The API asks Gemini to return a sentiment label, score, and theme.
4. The dashboard displays the individual results and an overall summary.
5. The user can save the results to the local SQLite database.

## Requirements

- Python 3.12 or newer
- [`uv`](https://docs.astral.sh/uv/)
- A Google Gemini API key

## Setup

Clone the repository, enter the project directory, and install the locked
dependencies:

```bash
uv sync
```

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

The Google Gen AI SDK also supports `GOOGLE_API_KEY`. Keep API keys out of
source control.

## Run the application

The backend and dashboard run as separate processes. Start the API in one
terminal:

```bash
uv run fastapi dev api.py
```

The API will be available at `http://127.0.0.1:8000`. Its interactive OpenAPI
documentation is available at `http://127.0.0.1:8000/docs`.

In a second terminal, start the dashboard:

```bash
uv run streamlit run app.py
```

Open the URL printed by Streamlit, paste one customer review per line, and
select **Analyze**. Select **Save to database** to store the current results.

## API usage

Analyze a single review directly:

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"The delivery was fast and the food was excellent."}'
```

Example response:

```json
{
  "label": "positive",
  "score": 5,
  "theme": "delivery"
}
```

The generated values may vary. The API constrains the response to:

- `label`: `positive`, `negative`, or `neutral`
- `score`: an integer from 1 to 5
- `theme`: one lowercase word describing the main topic

## Dashboard features

- Analyze multiple reviews in one batch
- View results in a table
- See the average score and percentage of positive reviews
- Identify the most common customer theme
- Save results locally
- Browse all previously saved reviews
- Continue a batch if an individual request fails

## Project structure

```text
.
├── api.py                         # FastAPI service and Gemini integration
├── app.py                         # Streamlit dashboard
├── database.py                    # SQLite initialization and queries
├── feedback.db                    # Local review database
├── pyproject.toml                 # Project metadata and dependencies
├── uv.lock                        # Reproducible dependency lockfile
└── src/project_feedback_analyzer/ # Installable Python package
```

## Configuration notes

- The dashboard expects the API at `http://127.0.0.1:8000/analyze`. Update
  `API_URL` in `app.py` if the backend runs elsewhere.
- The API currently uses the model configured in `api.py`.
- SQLite data is stored in `feedback.db` relative to the directory from which
  the application is started.
- Saving the same analysis more than once creates duplicate database rows.

## Troubleshooting

**The dashboard shows `error` for a review**

Confirm that the FastAPI process is running, the API URL is correct, and your
Gemini API key is available in `.env`.

**The API fails during startup or analysis**

Run `uv sync` again, check the API key, and review the backend terminal output
for the detailed error.

**Saved history is missing**

Start the app from the project root so it reads and writes the expected
`feedback.db` file.
