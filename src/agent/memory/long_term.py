"""Long-term memory: PostgreSQL store with semantic search.

Stores customer facts, preferences, and interaction history that persists
across conversation threads. Organized by namespace:

    (customer_id, "facts") → user preferences, past issues, communication style

Supports semantic search via Gemini embeddings so the agent can find
relevant facts using natural language queries.
"""

from __future__ import annotations

import logging

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.store.memory import InMemoryStore

from agent.settings import settings

logger = logging.getLogger(__name__)

_store: InMemoryStore | None = None
_embeddings: GoogleGenerativeAIEmbeddings | None = None


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    """Get or create the Gemini embeddings singleton."""
    global _embeddings
    if _embeddings is None:
        _embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key,
        )
    return _embeddings


def get_store() -> InMemoryStore:
    """Get or create the long-term memory store singleton.

    Uses InMemoryStore for development. In production, swap to
    ``AsyncPostgresStore`` for persistent cross-session memory.
    """
    global _store
    if _store is not None:
        return _store

    embeddings = get_embeddings()

    _store = InMemoryStore(
        index={
            "dims": settings.embedding_dims,
            "embed": embeddings,
            "fields": ["text"],
        },
    )
    logger.info("Long-term memory store initialized")
    return _store
