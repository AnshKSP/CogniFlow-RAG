from __future__ import annotations

from typing import List, Dict, Any

from google import genai
from google.genai import types
from pinecone import Pinecone, ServerlessSpec

from app.core.config import settings


class PineconeVectorStore:
    def __init__(self) -> None:
        # Gemini client (for embeddings)
        self._gemini = genai.Client(api_key=settings.GEMINI_API_KEY)

        # Pinecone client
        self._pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self._index_name = settings.PINECONE_INDEX_NAME

        # Ensure index exists with the correct dimension
        self._ensure_index()
        self._index = self._pc.Index(self._index_name)

    def _ensure_index(self) -> None:
        """
        Create the Pinecone index if it does not exist.

        Expects:
        - settings.VECTOR_DIMENSION == 768  (Gemini embeddings)
        - settings.PINECONE_ENV e.g. 'us-east-1'
        """
        existing = [idx["name"] for idx in self._pc.list_indexes()]
        if self._index_name in existing:
            return

        self._pc.create_index(
            name=self._index_name,
            dimension=settings.VECTOR_DIMENSION,  # 768 for gemini-embedding-001
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=settings.PINECONE_ENV,
            ),
        )

    def _embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of texts using Gemini embeddings.

        Returns a list of embedding vectors (list[float]) in the same order
        as the input texts.
        """
        result = self._gemini.models.embed_content(
            model=settings.GEMINI_EMBED_MODEL,
            contents=texts,
            config=types.EmbedContentConfig(
                output_dimensionality=settings.VECTOR_DIMENSION
            ),
        )
        # result.embeddings is a list; each has .values
        return [e.values for e in result.embeddings]

    def add_documents(self, docs: List[Dict[str, Any]]) -> None:
        """
        Ingest documents into Pinecone.

        docs: list of dicts:
          {
            "id": str,
            "text": str,
            "metadata": dict (optional)
          }
        """
        if not docs:
            return

        texts = [d["text"] for d in docs]
        vectors = self._embed_texts(texts)

        items = []
        for doc, vec in zip(docs, vectors):
            metadata = doc.get("metadata", {}).copy()
            # Store original text for later context reconstruction
            if "text" not in metadata:
                metadata["text"] = doc["text"]

            items.append(
                {
                    "id": doc["id"],
                    "values": vec,
                    "metadata": metadata,
                }
            )

        self._index.upsert(vectors=items)

    def similarity_search(self, query: str, top_k: int = 5):
        """
        Embed the query with Gemini and return top_k most similar matches
        from Pinecone (with metadata).
        """
        query_vec = self._embed_texts([query])[0]
        result = self._index.query(
            vector=query_vec,
            top_k=top_k,
            include_metadata=True,
        )
        return result.matches
