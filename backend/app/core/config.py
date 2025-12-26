# backend/app/core/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# 1. Setup the path to the .env file
# This says: "Go up 3 levels from this file to find the backend folder"
env_path = Path(__file__).resolve().parent.parent.parent / ".env"

# 2. Force load the .env file
load_status = load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "CogniFlow RAG")
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

settings = Settings()

# Debugging: Print this only if this file is run directly
if __name__ == "__main__":
    print(f"Looking for .env at: {env_path}")
    print(f"File exists? {env_path.exists()}")
    print(f"Did environment load? {load_status}")