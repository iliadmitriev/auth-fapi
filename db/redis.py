import aioredis
from config.connection import REDIS_URL


async def app_init_redis(app):
    app.state.redis = aioredis.from_url(
        REDIS_URL
    )


async def app_dispose_redis(app):
    await app.state.redis.close()


async def get_redis_key(redis, key):
    async with redis.client() as conn:
        val = await conn.get(key)
    return val


async def set_redis_key(redis, key, value, expire=None):
    async with redis.client() as conn:
        if expire is None:
            res = await conn.set(key, value)
        else:
            res = await conn.set(key, value, ex=expire)
    return res
