import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI-App")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").strip().lower() == "true"
    ENV: str = os.getenv("ENV", "development")

    API_PREFIX: str = os.getenv("API_PREFIX", "/api")

    GOOGLE_API_KEY: str | None = os.getenv("GOOGLE_API_KEY")

    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is missing in environment variables")

    ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*").split(",")
    ALLOW_METHODS = os.getenv("ALLOW_METHODS", "*").split(",")
    ALLOW_HEADERS = os.getenv("ALLOW_HEADERS", "*").split(",")
    ALLOW_CREDENTIALS: bool = (
        os.getenv("ALLOW_CREDENTIALS", "true").strip().lower() == "true"
    )
