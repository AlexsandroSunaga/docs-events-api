import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

# DATA_DIR overrides the default (<repo root>/data), e.g. /app/data in Docker.
DATA_DIR = Path(os.environ.get("DATA_DIR") or Path(__file__).resolve().parents[3] / "data")
EVENTS = DATA_DIR / "events.jsonl"
EVENTS.parent.mkdir(parents=True, exist_ok=True)


class ViewEvent(BaseModel):
    documentId: str
    linkId: str | None = None
    viewerEmail: str | None = None
    pageNumber: int | None = Field(default=None, ge=1)
    userAgent: str | None = None


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
