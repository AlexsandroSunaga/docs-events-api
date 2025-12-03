import os

from fastapi import APIRouter

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("/status")
def integration_status():
    return {
        "hubspot": {"enabled": bool(os.getenv("HUBSPOT_API_KEY"))},
        "sendgrid": {"enabled": bool(os.getenv("SENDGRID_API_KEY"))},
        "clearbit": {"enabled": bool(os.getenv("CLEARBIT_API_KEY"))},
    }
