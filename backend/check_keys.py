# backend/check_keys.py
from app.core.config import settings

print("--- DIAGNOSTIC REPORT ---")
print(f"1. PROJECT_NAME:      {settings.PROJECT_NAME}")
print(f"2. OPENAI_API_KEY:    {'✅ Found' if settings.OPENAI_API_KEY else '❌ MISSING (None)'}")
print(f"3. PINECONE_API_KEY:  {'✅ Found' if settings.PINECONE_API_KEY else '❌ MISSING (None)'}")
print(f"4. PINECONE_INDEX:    {'✅ Found' if settings.PINECONE_INDEX_NAME else '❌ MISSING (None)'}")
print("-------------------------")