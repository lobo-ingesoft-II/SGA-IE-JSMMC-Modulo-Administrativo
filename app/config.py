# app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    AUTH_API_URL: str
    ESTUDIANTES_API_URL: str
    SECRET_KEY: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"  # 👈 esto carga automáticamente las variables

settings = Settings()