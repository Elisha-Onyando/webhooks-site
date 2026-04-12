import logging
from datetime import datetime, UTC
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

from src.modules.webhooks import repository

logger = logging.getLogger(__name__)

def create_webhook():
    webhook_id = uuid4()
    return webhook_id

async def process_incoming_webhook_request(db: Session, webhook_id: UUID, request: Request):
    content_type = request.headers.get("content-type", "")

    raw_body = await request.body()
    parsed_body = None
    body_type = "raw"

    try:
        if "application/json" in content_type:
            parsed_body = await request.json()
            body_type = "json"

        elif "application/x-www-form-urlencoded" in content_type:
            form = await request.form()
            parsed_body = dict(form)
            body_type = "form"

        elif "multipart/form-data" in content_type:
            form = await request.form()
            parsed_body = {k: str(v) for k, v in form.items()}
            body_type = "multipart"

        elif "text/" in content_type:
            parsed_body = raw_body.decode("utf-8", errors="ignore")
            body_type = "text"

        else:
            # fallback → binary or unknown
            parsed_body = raw_body.decode("utf-8", errors="ignore")
            body_type = "unknown"

    except Exception:
        # absolute fallback (never fail webhook ingestion)
        parsed_body = raw_body.decode("utf-8", errors="ignore")
        body_type = "error_fallback"

    data = {
        "webhook_id": webhook_id,
        "client_ip": request.client.host,
        "method": request.method,
        "headers": {k: str(v) for k, v in request.headers.items()},
        "query_params": dict(request.query_params.multi_items()),
        "body": parsed_body,
        "raw_body": raw_body.decode("utf-8", errors="ignore"),
        "body_type": body_type,
        "body_size": len(raw_body),
        "created_at": datetime.now(UTC)
    }
    return repository.save_webhook_request(db, data)


def fetch_webhook_requests(db: Session, webhook_id: UUID):
    return repository.get_requests_by_webhook_id(db, webhook_id)

def delete_webhook_request(webhook_id: UUID, request_id: UUID, db: Session):
    deleted_request = repository.delete_webhook_request(db, webhook_id, request_id)
    if not deleted_request:
        raise HTTPException(status_code=404, detail="Request not found")

    return {"message": "Request deleted successfully"}

def delete_all_webhook_requests(db: Session, webhook_id: UUID):
    return repository.clear_webhook_requests(db, webhook_id)