import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY: str = os.environ.get("GOOGLE_API_KEY")
    OPENWEATHERMAP_API_KEY: str = os.environ.get("OPENWEATHERMAP_API_KEY")

settings = Settings()