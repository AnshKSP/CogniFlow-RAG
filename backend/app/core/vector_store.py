# backend/app/core/vector_store.py
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone  # Import the official client
from app.core.config import settings

def get_vector_store():
    """
    Returns a connection to the Pinecone Vector Database.
    Explicitly initializes the Sync client to avoid async errors.
    """
    
    # 1. Initialize the Embedding Model
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=settings.OPENAI_API_KEY
    )

    # 2. Explicitly create the Pinecone Client (The Fix)
    # We force the use of the Synchronous client here
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    
    # 3. Target the specific Index
    index = pc.Index(settings.PINECONE_INDEX_NAME)

    # 4. Create the Vector Store using the explicit index
    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings
    )

    return vector_store