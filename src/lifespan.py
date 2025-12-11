from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from redis.asyncio import Redis

from src.settings import settings


async def _setup_redis(app: FastAPI) -> None:
    redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
    if not await redis_client.ping():  # type: ignore
        raise RuntimeError("Redis is not reachable")
    app.state.redis_client = redis_client


@asynccontextmanager
async def lifespan_setup(app: FastAPI) -> AsyncGenerator[None, None]:
    await _setup_redis(app)
    yield
    await app.state.redis_client.close()
