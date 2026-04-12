from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from src.core.database import get_db
from src.modules.webhooks.schemas import CreateWebhookResponseDto, WebhookRequestDto
from src.modules.webhooks import service

webhook_router = APIRouter(prefix="/webhooks", tags=["Webhooks"])
requests_router = APIRouter(prefix="/webhooks", tags=["Requests"])

@webhook_router.post("", response_model=CreateWebhookResponseDto)
def create_webhook(request: Request):
    """Creates webhook url"""
    hook_id = service.create_webhook()
    return CreateWebhookResponseDto(
        webhook_id=hook_id,
        webhook_url=f"{request.base_url}webhooks/{hook_id}"
    )

@requests_router.post("/{webhook_id}", response_model=None)
async def receive_webhook_request(webhook_id: UUID, request: Request, db: Session = Depends(get_db)):
    """Receives and processes a webhook request"""
    await service.process_incoming_webhook_request(db, webhook_id, request)
    return {"status":"Webhook request received successfully"}


@webhook_router.get("/{webhook_id}/requests", response_model=list[WebhookRequestDto])
def fetch_webhook_requests(webhook_id: UUID, db: Session = Depends(get_db)):
    """Fetches webhook requests list"""
    return service.fetch_webhook_requests(db, webhook_id=webhook_id)

@webhook_router.delete("/{webhook_id}/requests/clear", response_model=None)
def delete_all_webhook_requests(webhook_id: UUID, db: Session = Depends(get_db)):
    """Deletes all webhook requests"""
    deleted = service.delete_all_webhook_requests(db, webhook_id=webhook_id)
    return {"status": f"{deleted} Webhook requests deleted successfully"}

@webhook_router.delete("/{webhook_id}/requests/{request_id}", response_model=None)
def delete_webhook_request(webhook_id: UUID, request_id: UUID, db: Session = Depends(get_db)):
    """Deletes a webhook request"""
    return service.delete_webhook_request(webhook_id, request_id, db)