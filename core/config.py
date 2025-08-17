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

    class Config:
        env_file = "dev.env"
        env_file_encoding = "utf-8"

# Instancia global
settings = Settings() # type: ignore

print(settings.DATABASE_URL, 'bostero', 'funcionoooooo')