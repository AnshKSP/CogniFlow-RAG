class Settings:
    # Core API keys
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    GEMINI_API_KEY: str

    # Pinecone configuration
    PINECONE_ENV: str
    PINECONE_INDEX_NAME: str

    # Models / vector config
    EMBEDDING_MODEL: str
    VECTOR_DIMENSION: int
    GEMINI_CHAT_MODEL: str
    GEMINI_EMBED_MODEL: str

    def __init__(self) -> None:
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

        self.PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")
        self.PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "cogniflow-index")

        # Keep VECTOR_DIMENSION = 768 for gemini-embedding-001 (typical size)
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        self.VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", "768"))

        self.GEMINI_CHAT_MODEL = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.0-flash")
        self.GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-001")

        self._validate()

    def _validate(self) -> None:
        missing: list[str] = []
        for field in ["PINECONE_API_KEY", "GEMINI_API_KEY"]:
            if not getattr(self, field):
                missing.append(field)

        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Check that your .env file exists at project root and variables are set."
            )
