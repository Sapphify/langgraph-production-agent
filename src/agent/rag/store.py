"""RAG vectorstore: PGVector setup for policy document retrieval.

Stores chunked and embedded company policy documents. The ``search_policies``
tool queries this vectorstore when the agent needs to reference company rules.
"""

from __future__ import annotations

import logging

from langchain_core.vectorstores import InMemoryVectorStore

from agent.memory.long_term import get_embeddings

logger = logging.getLogger(__name__)

_vectorstore: InMemoryVectorStore | None = None


def get_vectorstore() -> InMemoryVectorStore:
    """Get or create the RAG vectorstore singleton.

    Uses InMemoryVectorStore for development. In production, swap to
    ``PGVector`` for persistent storage.
    """
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = InMemoryVectorStore(embedding=get_embeddings())
        logger.info("RAG vectorstore initialized")
    return _vectorstore


def get_retriever(k: int = 4):
    """Get a retriever that returns the top-k most relevant documents."""
    return get_vectorstore().as_retriever(search_kwargs={"k": k})
