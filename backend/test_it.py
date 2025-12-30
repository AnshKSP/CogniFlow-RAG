from __future__ import annotations

from typing import List

from google import genai

from app.core.config import settings
from app.core.vector_store import PineconeVectorStore


client = genai.Client(api_key=settings.GEMINI_API_KEY)


def build_context_from_matches(matches, max_chars: int = 1500) -> str:
    chunks: List[str] = []
    total = 0
    for m in matches:
        meta = m.metadata or {}
        text = meta.get("text") or meta.get("chunk_text") or ""
        if not text:
            continue
        if total + len(text) > max_chars:
            break
        chunks.append(text)
        total += len(text)
    return "\n\n".join(chunks)


def ingest_example_docs() -> None:
    store = PineconeVectorStore()
    docs = [
        {
            "id": "doc1",
            "text": "CogniFlow-RAG is an agentic Retrieval-Augmented Generation system that uses Pinecone as a vector database.",
            "metadata": {"source": "internal"},
        },
        {
            "id": "doc2",
            "text": "The backend is written in Python and uses Gemini 2.0 Flash as the primary large language model.",
            "metadata": {"source": "internal"},
        },
    ]
    store.add_documents(docs)
    print("Ingested example docs into Pinecone with Gemini embeddings.")


def ask(query: str) -> None:
    store = PineconeVectorStore()
    matches = store.similarity_search(query, top_k=3)
    context = build_context_from_matches(matches)

    user_prompt = f"""
Use the following context to answer the user's question.
If the answer is not in the context, say you are not sure.

Context:
{context}

Question: {query}
"""

    response = client.models.generate_content(
        model=settings.GEMINI_CHAT_MODEL,
        contents=user_prompt,
    )

    print("Answer:\n")
    print(response.text)


if __name__ == "__main__":
    ingest_example_docs()
    ask("What does CogniFlow-RAG use as a vector database?")
