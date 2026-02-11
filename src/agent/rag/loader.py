"""Document loader: chunk and embed policy documents into the vectorstore."""

from __future__ import annotations

import logging
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from agent.rag.store import get_vectorstore

logger = logging.getLogger(__name__)

POLICIES_DIR = Path(__file__).resolve().parents[3] / "data" / "policies"


def ingest_policies(directory: Path = POLICIES_DIR) -> int:
    """Load markdown policy files, chunk them, and add to the vectorstore.

    Returns the number of chunks ingested.
    """
    if not directory.exists():
        logger.warning("Policy directory not found: %s", directory)
        return 0

    loader = DirectoryLoader(
        str(directory),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()
    logger.info("Loaded %d policy documents from %s", len(docs), directory)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(docs)
    logger.info("Split into %d chunks", len(chunks))

    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)
    logger.info("Ingested %d chunks into vectorstore", len(chunks))

    return len(chunks)
