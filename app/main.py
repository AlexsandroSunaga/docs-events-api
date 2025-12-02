import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

EVENTS = Path(__file__).resolve().parent.parent / "data" / "events.jsonl"
EVENTS.parent.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Document Events API", version="1.0.0", description="Auxiliary event sink for link/view analytics.")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class ViewEvent(BaseModel):
    documentId: str
    linkId: str | None = None
    viewerEmail: str | None = None
    pageNumber: int | None = Field(default=None, ge=1)
    userAgent: str | None = None


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "sink": "jsonl"}


@app.post("/api/v1/events/view")
def record_view(body: ViewEvent) -> dict:
    row = {
        "id": str(uuid.uuid4()),
        "type": "view",
        "at": datetime.now(timezone.utc).isoformat(),
        **body.model_dump(),
    }
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return {"accepted": True, "id": row["id"]}


@app.get("/api/v1/events/summary")
def summary() -> dict:
    if not EVENTS.exists():
        return {"views": 0, "documents": 0}
    docs: set[str] = set()
    count = 0
    for line in EVENTS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        count += 1
        docs.add(json.loads(line).get("documentId", ""))
    return {"views": count, "documents": len(docs)}
