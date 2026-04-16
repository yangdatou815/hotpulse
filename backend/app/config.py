import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "HotPulse API"
    api_prefix: str = "/api/v1"
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://hotpulse:hotpulse@db:5432/hotpulse",
    )


settings = Settings()
