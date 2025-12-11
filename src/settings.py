from pydantic import Field
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = Field(
        default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0")
    )


settings = Settings()
