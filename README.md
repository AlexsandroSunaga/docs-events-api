# Document Events API (FastAPI)

A document view analytics API: records document/link view events to a JSONL file (`data/events.jsonl`) and returns a simple summary (total views, distinct documents).

There are two entry points in this repo:

| Entry | Location | Contents |
|---|---|---|
| Legacy | `app.main:app` (repo root, `app/`) | health, view event, summary |
| Backend (current) | `backend/` (`src.main:backend_app`) | same, plus integrations status |

## Run

Legacy entry (from the repo root):

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8040
```

Backend entry:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
mkdir data                                           # SQLite file location (./data/app.db)
PYTHONPATH=src uvicorn src.main:backend_app --reload --port 8040   # PowerShell: $env:PYTHONPATH="src"
```

Interactive docs: http://127.0.0.1:8040/docs. The Docker image is built from the repository root (`docker compose up --build`, or `docker build -f backend/Dockerfile -t docs-events-api .`) and serves the backend entry on port 8000. Events are stored in the `/app/data` volume. The data directory can be overridden with the `DATA_DIR` environment variable. Events are written to `data/events.jsonl` at the repository root when running locally.

## Endpoints

- `GET /health`
- `POST /api/v1/events/view`
- `GET /api/v1/events/summary`
- `GET /api/v1/integrations/status` (backend entry only)

## Examples

```bash
curl -X POST http://127.0.0.1:8040/api/v1/events/view \
  -H "Content-Type: application/json" \
  -d '{"documentId":"doc_123","linkId":"lnk_9","viewerEmail":"reader@example.com","pageNumber":3}'

curl http://127.0.0.1:8040/api/v1/events/summary
```

## Tests

Covers both the legacy entry (`app.main:app`) and the backend entry (`src.main:backend_app`).

```bash
pip install -r requirements.txt -r backend/requirements.txt -r requirements-dev.txt
python -m pytest -q
```

## Author

**Alexsandro Sunaga**

## License

MIT License — see [LICENSE](LICENSE).
