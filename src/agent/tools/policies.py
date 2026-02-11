"""Tool: search company policies via RAG.

This is the agentic RAG entry point. The agent decides *when* to search
company policies — it's not forced on every query. The tool queries a
PGVector vectorstore containing chunked policy documents.
"""

from __future__ import annotations

from langchain_core.tools import tool


@tool
def search_policies(query: str) -> str:
    """Search company policies, FAQ, and product documentation.

    Use this when customers ask about returns, shipping, warranty,
    account policies, or product information. Provide a clear,
    specific query describing what you need to know.
    """
    from agent.rag.store import get_retriever

    retriever = get_retriever()
    docs = retriever.invoke(query)

    if not docs:
        return "No matching policies found. Consider escalating to a human agent."

    results = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown")
        results.append(f"[Policy {i} | {source}]\n{doc.page_content}")

    return "\n\n---\n\n".join(results)
