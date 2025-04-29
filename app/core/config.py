import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache
from typing import List, Optional

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Multi-Agent FastAPI Backend"
    API_V1_STR: str = "/v1"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    AGENT_LLM_MODEL: str = os.getenv("AGENT_LLM_MODEL")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 días
    
    class Config:
        case_sensitive = True
        env_file = '.env'

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

if not settings.OPENAI_API_KEY:
    print("ADVERTENCIA: OPENAI_API_KEY no está configurada en las variables de entorno.")