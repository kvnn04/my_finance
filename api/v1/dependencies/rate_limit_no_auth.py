from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from core.rate_limit import check_rate_limit_ip
from core.redis_client import r  # tu cliente redis

class RateLimitIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host # type: ignore
        try:
            await check_rate_limit_ip(r, client_ip)
        except HTTPException as e:
            # Devuelve un JSONResponse en lugar de lanzar la excepción
            return JSONResponse(
                status_code=e.status_code,
                # content={"detail": e.detail}
                content={"detail": 'Te pasaste pa, espera un toque'}
            )
        # Si pasa el rate limit, continua normalmente
        response = await call_next(request)
        return response

# app.add_middleware(RateLimitIPMiddleware)
