import time
import redis.asyncio as redis
from fastapi import HTTPException, Depends
from api.v1.routes.auth import get_current_user
from db.models.user import User
from sqlalchemy.orm import Session
from core.redis_client import r
from core.config import settings

def get_user_rate_limit(user: User) -> tuple[int, int]:
    """Devuelve (máx_requests, ventana_segundos) según el plan"""
    return user.plan.requests_per_window, user.plan.rate_limit_window
def rate_limit():
    """Decorador para endpoints"""
    def decorator(func):
        async def wrapper(
            user: User = Depends(get_current_user),  # ✅ acá
            *args,
            **kwargs
        ):
            await check_rate_limit(r, user)
            return await func(user, *args, **kwargs)
        return wrapper
    return decorator



async def check_rate_limit(redis: redis.Redis, user: User):
    key = f"rate_limit:{user.id}"
    max_tokens, window = get_user_rate_limit(user)
    now = int(time.time())

    data = await redis.hgetall(key) # type: ignore
    if not data:
        await redis.hset(key, mapping={"tokens": max_tokens - 1, "last": now}) # type: ignore
        await redis.expire(key, window)
        return

    tokens = int(data.get("tokens", max_tokens))
    last = int(data.get("last", now))

    elapsed = now - last
    refill = int(elapsed * (max_tokens / window))
    tokens = min(tokens + refill, max_tokens)

    if tokens <= 0:
        raise HTTPException(status_code=429, detail="Rate limit excedido")

    tokens -= 1
    await redis.hset(key, mapping={"tokens": tokens, "last": now}) # type: ignore
    await redis.expire(key, window)

# async def check_rate_limit_ip(redis: redis.Redis, ip: str, max_tokens: int = 10, window: int = 60):
async def check_rate_limit_ip(redis: redis.Redis, ip: str):
    """
    Rate limit para usuarios no autenticados, basado en IP.
    
    :param redis: cliente Redis
    :param ip: IP del cliente
    :param max_tokens: cantidad máxima de requests por ventana
    :param window: ventana de tiempo en segundos
    """
    window = settings.RATE_LIMIT_WINDOW
    max_tokens = settings.RATE_LIMIT_MAX_TOKENS
    key = f"rate_limit_ip:{ip}"
    now = int(time.time())

    data = await redis.hgetall(key) # type: ignore
    if not data:
        await redis.hset(key, mapping={"tokens": max_tokens - 1, "last": now}) # type: ignore
        await redis.expire(key, window)
        return

    tokens = int(data.get("tokens", max_tokens))
    last = int(data.get("last", now))

    elapsed = now - last
    refill = int(elapsed * (max_tokens / window))
    tokens = min(tokens + refill, max_tokens)

    if tokens <= 0:
        raise HTTPException(status_code=429, detail="Rate limit excedido para IP")

    tokens -= 1
    await redis.hset(key, mapping={"tokens": tokens, "last": now}) # type: ignore
    await redis.expire(key, window)
