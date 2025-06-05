import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY: str = os.environ.get("GOOGLE_API_KEY")
    BACKEND_CORS_ORIGINS = os.environ.get("BACKEND_CORS_ORIGINS")

settings = Settings()