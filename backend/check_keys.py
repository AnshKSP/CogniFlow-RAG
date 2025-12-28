from app.core.config import settings


def main() -> None:
    print("=== CogniFlow-RAG settings check ===")
    print(settings.debug_summary())


if __name__ == "__main__":
    main()
