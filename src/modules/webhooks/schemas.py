from datetime import datetime
from typing import Dict, Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateWebhookResponseDto(BaseModel):
    webhook_id: UUID
    webhook_url: str

class WebhookRequestDto(BaseModel):
    request_id: UUID = Field(alias="id")
    webhook_id: UUID
    client_ip: str
    method: str
    headers: Dict[str, Any]
    query_params: Dict[str, Any]
    body: Any
    raw_body: Any
    body_type: str
    body_size: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)