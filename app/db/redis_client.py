
# redis_client.py
from redis import asyncio as aioredis
from redis.asyncio import Redis
from app.core.config import settings

# Initialize the Redis client globally or in a function
def get_redis_client() -> Redis:
    # Use from_url for easy configuration. decode_responses=True decodes responses to strings
    redis_client = aioredis.from_url(
        settings.REDIS_URL,
        decode_responses=True
    )
    return redis_client

