# backend/test_it.py
from app.core.vector_store import get_vector_store

print("🔌 Connecting to Pinecone...")

try:
    # Try to grab the database connection
    db = get_vector_store()
    print("✅ Connection Successful!")
    
    # Try to add a fake memory
    print("📝 Saving a test memory...")
    db.add_texts(
        texts=["CogniFlow is starting up!"],
        metadatas=[{"author": "Ansh"}]
    )
    print("🚀 SUCCESS! Memory saved to cloud.")
    
except Exception as e:
    print(f"❌ ERROR: {e}")