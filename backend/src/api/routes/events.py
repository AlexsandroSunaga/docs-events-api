from fastapi import APIRouter

from src.services.event_store import ViewEvent, record_view, summary

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/view")
def view(body: ViewEvent) -> dict:
    return record_view(body)


@router.get("/summary")
def events_summary() -> dict:
    return summary()
