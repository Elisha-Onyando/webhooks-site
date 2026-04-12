import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.api.routes import api_router
from src.core.config import settings
from src.core.database import test_db_connection, Base, engine
from src.web.routes import ui_router

BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

#Lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")

    # Test DB Connection
    test_db_connection()

    # logger.info("Creating tables if not exists...")
    # Base.metadata.create_all(bind=engine)

    logger.info("Application startup complete")

    yield
    logger.info("Application shutdown complete")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

# API Routes
app.include_router(api_router)

# UI Routes
app.include_router(ui_router)

# MOUNT STATIC FILES
app.mount("/static", StaticFiles(directory=BASE_DIR/"web"/"static"), name="static")