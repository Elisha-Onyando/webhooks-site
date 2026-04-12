import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    app_name: str = os.getenv("APP_NAME")
    app_version: str = os.getenv("APP_VERSION")
    api_version: str = os.getenv("API_VERSION")
    
    # DB DETAILS
    db_url: str = os.getenv("DB_URL")
    db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_host: str = os.getenv("DB_HOST")
    db_port: int = os.getenv("DB_PORT")
    ssl_mode: str = os.getenv("SSL_MODE")

settings = Settings()