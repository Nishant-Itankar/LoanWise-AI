import os

from dotenv import load_dotenv


load_dotenv()


DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME", "")
DATABASE_USER = os.getenv("DATABASE_USER", "")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")

APP_ENV = os.getenv("APP_ENV", "development")

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "")