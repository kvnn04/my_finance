from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default="Finance API")
    DEBUG: bool = Field(default=True)

    # Base de datos
    DATABASE_URL: str = Field(..., description="Database connection URL")

    # Seguridad / JWT
    SECRET_KEY: str = Field(..., description="Secret key for JWT signing")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24)  # 1 día
    ALGORITHM: str = Field(default="HS256", description="JWT signing algorithm")
    
    # Configuración de CORS
    BACKEND_CORS_ORIGINS: List[str] = Field(default=["*"])

     # Redis
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)

    # Rate limits (requests por ventana)
    RATE_LIMIT_FREE: int = Field(default=5)
    RATE_LIMIT_PREMIUM: int = Field(default=20)
    RATE_LIMIT_WINDOW: int = Field(default=60)  # segundos
    RATE_LIMIT_MAX_TOKENS: int = Field(default=5)



    class Config:
        env_file = "dev.env"
        env_file_encoding = "utf-8"

# Instancia global
settings = Settings() # type: ignore

print(settings.DATABASE_URL, 'bostero', 'funcionoooooo')