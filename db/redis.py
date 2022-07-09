"""
Redis module.
"""
from typing import Optional

import aioredis
from aioredis import Redis
from fastapi import FastAPI

from config.connection import REDIS_URL


async def app_init_redis(app: FastAPI) -> None:
    """Init redis connection pool.

    Args:
        app: FastAPI application

    Returns:
        None
    """
    app.state.redis = aioredis.from_url(
        REDIS_URL
    )


async def app_dispose_redis(app: FastAPI) -> None:
    """Disposes redis connection pool.

    Args:
        app: FastAPI application.

    Returns:
        None
    """
    await app.state.redis.close()


async def get_redis_key(redis: Redis, key: str) -> Optional[str]:
    """Read redis key.

    Args:
        redis: redis database connection
        key: key

    Returns:
        value if found, None - otherwise
    """
    async with redis.client() as conn:
        val = await conn.get(key)
    return val


async def set_redis_key(
        redis: Redis, key: str, value: str,
        expire: Optional[int] = None
) -> bool:
    """Set redis key with expiration.

    Args:
        redis: redis connection pool object
        key: key to set
        value: value to set
        expire: expiration (seconds)

    Returns:
        True - success, False - otherwise
    """
    async with redis.client() as conn:
        if expire is None:
            res = await conn.set(key, value)
        else:
            res = await conn.set(key, value, ex=expire)
    return res
