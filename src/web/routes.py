from uuid import UUID

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.modules.webhooks import service
from src.core.database import get_db

ui_router = APIRouter(prefix="", tags=["UI"])
templates = Jinja2Templates(directory="src/web/templates")

@ui_router.get("/", response_class=HTMLResponse, response_model=None, include_in_schema=False)
def index_page(request: Request):
    return templates.TemplateResponse(name="index.html", request=request, media_type="text/html")

@ui_router.get("/webhooks/{webhook_id}", response_model=None, include_in_schema=False)
def webhook_details_page(request: Request, webhook_id: UUID, db: Session = Depends(get_db)):
    webhook_requests = service.fetch_webhook_requests(db, webhook_id)
    return templates.TemplateResponse(name="inspector/webhook_details.html", request=request, context={
        "webhook_id": webhook_id,
        "webhook_requests": webhook_requests
    })