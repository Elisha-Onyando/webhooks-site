import logging
import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base

from src.core.config import settings

database_uri = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}?sslmode={settings.ssl_mode}"

logger = logging.getLogger(__name__)

engine = create_engine(
    url=database_uri,
    pool_size=10,
    max_overflow=10,
    pool_timeout=10,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()

def test_db_connection(retries: int = 3, delay: int = 2):
    """
    Test database connection with retries and delay.
    Throws exception if connection retries fail.
    """
    attempts = 0
    while attempts < retries:
        try:
            logger.info(f"Attempting database connection (attempt {attempts + 1}/{retries})...")
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                logger.info(f"Database connection established successfully.")
                return True

        except OperationalError as e:
            attempts += 1
            logger.error(f"Database connection failed: {e.orig}.")
            if attempts < retries:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.critical(f"All database connection attempts failed.")
                return False
    return None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()