"""Ingest policy documents into the RAG vectorstore."""

from agent.rag.loader import ingest_policies

if __name__ == "__main__":
    count = ingest_policies()
    print(f"Ingested {count} document chunks into the vectorstore.")
