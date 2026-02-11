"""Application settings loaded from environment variables."""

from __future__ import annotations

import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """All configuration lives here. Loaded from .env file."""

    # Google Gemini
    google_api_key: str = ""
    model_name: str = "gemini-2.0-flash"
    embedding_model: str = "models/gemini-embedding-001"
    embedding_dims: int = 768
    temperature: float = 0.0

    # PostgreSQL
    postgres_uri: str = "postgresql://localhost:5432/customer_service_agent"

    # LangSmith (optional)
    langsmith_api_key: str = ""
    langsmith_project: str = "customer-service-agent"
    langsmith_tracing: bool = True

    # Logging
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s | %(name)-25s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
