"""Agent state schema.

This is the single source of truth for all data flowing through the graph.
Every node reads from and writes to this state.
"""

from __future__ import annotations

from langgraph.graph import MessagesState


class AgentState(MessagesState):
    """Customer service agent state.

    Inherits ``messages`` from MessagesState with the ``add_messages`` reducer,
    which appends new messages and deduplicates by ID.

    All other fields use the default *overwrite* reducer — the latest value wins.
    """

    # ── Customer context ──────────────────────────────────────────────
    customer_id: str
    """Identifier for the current customer (set at conversation start)."""

    customer_facts: list[str]
    """Facts loaded from long-term memory (preferences, past issues, etc.)."""

    # ── Order tracking ────────────────────────────────────────────────
    current_order: dict | None
    """Order details populated by the lookup_order tool."""

    # ── Human-in-the-loop ─────────────────────────────────────────────
    pending_approval: dict | None
    """The tool call dict waiting for manager approval."""

    approval_response: str
    """Manager's response: 'approved' or the rejection reason."""
