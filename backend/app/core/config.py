from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# This file: backend/app/core/config.py
# Project root: three levels up
ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = ROOT_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()


class Settings:
    # API keys
    PINECONE_API_KEY: str
    GEMINI_API_KEY: str

    # Pinecone configuration
    PINECONE_ENV: str
    PINECONE_INDEX_NAME: str

    # Models / vector config
    GEMINI_CHAT_MODEL: str
    GEMINI_EMBED_MODEL: str
    VECTOR_DIMENSION: int

    def __init__(self) -> None:
        # Keys
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

        # Pinecone
        self.PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")
        self.PINECONE_INDEX_NAME = os.getenv(
            "PINECONE_INDEX_NAME", "cogniflow-gemini-idx"
        )

        # Gemini models
        self.GEMINI_CHAT_MODEL = os.getenv(
            "GEMINI_CHAT_MODEL", "gemini-2.0-flash"
        )
        self.GEMINI_EMBED_MODEL = os.getenv(
            "GEMINI_EMBED_MODEL", "gemini-embedding-001"
        )

        # Vector dimension (must match Pinecone index and Gemini embeddings)
        self.VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", "768"))

        self._validate()

    def _validate(self) -> None:
        missing: list[str] = []
        for field in ["PINECONE_API_KEY", "GEMINI_API_KEY"]:
            if not getattr(self, field):
                missing.append(field)

        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Check your .env at project root."
            )

    def debug_summary(self) -> str:
        return (
            "Settings("
            f"PINECONE_API_KEY_set={bool(self.PINECONE_API_KEY)}, "
            f"GEMINI_API_KEY_set={bool(self.GEMINI_API_KEY)}, "
            f"PINECONE_ENV='{self.PINECONE_ENV}', "
            f"PINECONE_INDEX_NAME='{self.PINECONE_INDEX_NAME}', "
            f"GEMINI_CHAT_MODEL='{self.GEMINI_CHAT_MODEL}', "
            f"GEMINI_EMBED_MODEL='{self.GEMINI_EMBED_MODEL}', "
            f"VECTOR_DIMENSION={self.VECTOR_DIMENSION}"
            ")"
        )


settings = Settings()
