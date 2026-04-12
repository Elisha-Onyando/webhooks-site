from uuid import UUID

from sqlalchemy.orm import Session

from src.modules.webhooks.models import WebhookRequest

def save_webhook_request(db: Session, data: dict):
    request = WebhookRequest(**data)
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

def get_requests_by_webhook_id(db: Session, webhook_id: UUID):
    return db.query(WebhookRequest)\
            .filter(WebhookRequest.webhook_id == webhook_id)\
            .order_by(WebhookRequest.created_at.desc())\
            .all()

def delete_webhook_request(db: Session, webhook_id: UUID, request_id: UUID):
    record = db.query(WebhookRequest) \
            .filter(WebhookRequest.webhook_id == webhook_id) \
            .filter(WebhookRequest.id == request_id) \
            .first()

    if not record:
        return None

    db.delete(record)
    db.commit()
    return record

def clear_webhook_requests(db: Session, webhook_id: UUID):
    deleted = db.query(WebhookRequest) \
            .filter(WebhookRequest.webhook_id == webhook_id) \
            .delete(synchronize_session=False)

    db.commit()

    return deleted