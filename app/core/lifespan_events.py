from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from redis.asyncio import Redis
from app.db.redis_client import get_redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect Redis on startup
    app.state.redis = get_redis_client()
    try:
        await app.state.redis.ping() # Optional: check connection
        print("Redis connected successfully!")
    except Exception as e:
        print(f"Redis connection failed: {e}")
    yield
    # Close connection on shutdown
    await app.state.redis.close()