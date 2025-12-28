# redis_client.py
from redis import asyncio as aioredis
from redis.asyncio import Redis
from app.core.config import settings

class MockRedis:
    def __init__(self):
        print(" Using MockRedis (In-Memory Fallback)")
        self._cache = {}

    async def ping(self):
        return True

    async def close(self):
        pass

    async def get(self, key):
        return self._cache.get(key)

    async def set(self, key, value, *args, **kwargs):
        self._cache[key] = value
        return True

    async def getex(self, key, *args, **kwargs):
        return self._cache.get(key)

    async def setex(self, key, time, value):
        self._cache[key] = value
        return True
        
    async def delete(self, key):
        if key in self._cache:
            del self._cache[key]
        return 1

# Initialize the Redis client globally or in a function
def get_redis_client() -> Redis:
    # Use from_url for easy configuration. decode_responses=True decodes responses to strings
    redis_client = aioredis.from_url(
        settings.REDIS_URL,
        decode_responses=True
    )
    return redis_client

