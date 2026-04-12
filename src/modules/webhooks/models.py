from datetime import datetime, UTC
import uuid

from sqlalchemy import Column, UUID, String, JSON, DateTime, Integer, Text

from src.core.database import Base

class WebhookRequest(Base):
    __tablename__ = "webhook_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    webhook_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    client_ip = Column(String, index=True)
    method = Column(String, nullable=False)
    headers = Column(JSON, nullable=False)
    query_params = Column(JSON, nullable=False)
    body = Column(JSON, nullable=True)
    raw_body = Column(Text, nullable=True)
    body_type = Column(String, nullable=True)
    body_size = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))