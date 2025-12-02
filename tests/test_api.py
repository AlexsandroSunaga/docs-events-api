import json

import pytest
from fastapi.testclient import TestClient

import app.main as legacy_module
import src.services.event_store as backend_store
from src.main import backend_app

PREFIX = "/api/v1"


@pytest.fixture(params=["legacy", "backend"])
def client(request, tmp_path, monkeypatch):
    sink = tmp_path / "events.jsonl"
    if request.param == "legacy":
        monkeypatch.setattr(legacy_module, "EVENTS", sink)
        app = legacy_module.app
    else:
        monkeypatch.setattr(backend_store, "EVENTS", sink)
        app = backend_app
    with TestClient(app) as c:
        c.sink = sink
        yield c


def test_health(client):
    assert client.get("/health").json() == {"status": "ok", "sink": "jsonl"}


def test_summary_empty(client):
    assert client.get(f"{PREFIX}/events/summary").json() == {"views": 0, "documents": 0}


def test_record_view_and_summary(client):
    for doc in ("doc_1", "doc_1", "doc_2"):
        r = client.post(f"{PREFIX}/events/view", json={"documentId": doc, "pageNumber": 3})
        assert r.status_code == 200 and r.json()["accepted"] is True
    assert client.get(f"{PREFIX}/events/summary").json() == {"views": 3, "documents": 2}
    first = json.loads(client.sink.read_text(encoding="utf-8").splitlines()[0])
    assert first["type"] == "view" and first["documentId"] == "doc_1" and "at" in first


def test_view_validation_errors(client):
    assert client.post(f"{PREFIX}/events/view", json={}).status_code == 422
    bad_page = client.post(f"{PREFIX}/events/view", json={"documentId": "d", "pageNumber": 0})
    assert bad_page.status_code == 422


def test_backend_integrations_status():
    with TestClient(backend_app) as c:
        assert set(c.get(f"{PREFIX}/integrations/status").json()) == {"hubspot", "sendgrid", "clearbit"}
