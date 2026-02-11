"""Main graph: build, compile, and export the customer service agent.

This is the entry point referenced in ``langgraph.json``.
Exports ``graph`` — the compiled, ready-to-run agent.

Graph topology:
    START → respond → [route] → execute → respond → ... → remember → END
                           ↘ review → [route] → execute / respond
"""

from __future__ import annotations

import logging

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy

from agent.nodes.execute import run_tools
from agent.nodes.remember import save_memory
from agent.nodes.respond import call_model
from agent.nodes.review import human_review
from agent.routing import route_after_respond, route_after_review
from agent.state import AgentState

logger = logging.getLogger(__name__)


def build_graph() -> StateGraph:
    """Construct the StateGraph with all nodes and edges.

    This is separate from ``compile_graph`` so that tests can build
    the graph and compile it with their own checkpointer/store.
    """
    builder = StateGraph(AgentState)

    # ── Nodes ──────────────────────────────────────────────────────
    builder.add_node("respond", call_model, retry_policy=RetryPolicy(max_attempts=3))
    builder.add_node("execute", run_tools, retry_policy=RetryPolicy(max_attempts=2))
    builder.add_node("review", human_review)
    builder.add_node("remember", save_memory, retry_policy=RetryPolicy(max_attempts=2))

    # ── Edges ──────────────────────────────────────────────────────
    builder.add_edge(START, "respond")

    builder.add_conditional_edges("respond", route_after_respond, {
        "review": "review",
        "execute": "execute",
        "remember": "remember",
    })

    builder.add_conditional_edges("review", route_after_review, {
        "execute": "execute",
        "respond": "respond",
    })

    builder.add_edge("execute", "respond")
    builder.add_edge("remember", END)

    return builder


def compile_graph():
    """Compile the graph with a default in-memory checkpointer.

    For production, replace ``MemorySaver`` with ``AsyncPostgresSaver``
    from ``agent.memory.short_term`` and add a store from
    ``agent.memory.long_term``.
    """
    builder = build_graph()
    checkpointer = MemorySaver()

    return builder.compile(
        checkpointer=checkpointer,
    )


# ── The exported graph (referenced in langgraph.json) ──────────────
graph = compile_graph()
