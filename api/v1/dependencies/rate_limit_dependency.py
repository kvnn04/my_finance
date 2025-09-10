# --- Dependencia global de rate limit ---
from fastapi import Depends
from api.v1.routes.auth import get_current_user_2
from db.models.user import User
from core.rate_limit import check_rate_limit
from core.redis_client import r


async def rate_limit_dependency(current_user: User = Depends(get_current_user_2)):
    await check_rate_limit(r, current_user)
    return current_user
