from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from redis.asyncio import Redis
from app.db.redis_client import get_redis_client, MockRedis

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect Redis on startup
    try:
        app.state.redis = get_redis_client()
        await app.state.redis.ping() # Check connection
        print("Redis connected successfully!")
    except Exception as e:
        print(f"Redis connection failed: {e}")
        print(" Switching to MockRedis fallback...")
        app.state.redis = MockRedis()
        
    yield
    # Close connection on shutdown
    await app.state.redis.close()