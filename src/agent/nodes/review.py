"""Node: human-in-the-loop review for sensitive tool calls.

When the agent tries to process a refund or update an account, this node
pauses the graph using ``interrupt()``. A manager reviews the request and
either approves or rejects it. The graph resumes via ``Command(resume=...)``.

Key LangGraph concepts demonstrated:
- interrupt() pauses execution and checkpoints state
- The entire node re-executes from the start on resume
- The resume value becomes the return value of interrupt()
"""

from __future__ import annotations

import logging

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.types import interrupt

from agent.state import AgentState

logger = logging.getLogger(__name__)


async def human_review(state: AgentState) -> dict:
    """Pause for manager approval of a sensitive tool call."""
    last_message: AIMessage = state["messages"][-1]
    tool_call = last_message.tool_calls[0]

    logger.info(
        "Requesting manager approval for '%s' (args: %s)",
        tool_call["name"],
        tool_call["args"],
    )

    # ── This pauses the graph ──────────────────────────────────────
    # The caller receives the interrupt payload and must respond
    # with Command(resume="approve") or Command(resume="reject: reason")
    decision = interrupt({
        "question": f"Approve '{tool_call['name']}'?",
        "tool_name": tool_call["name"],
        "tool_args": tool_call["args"],
        "options": ["approve", "reject"],
    })
    # ── Graph resumes here when Command(resume=...) is sent ────────

    if decision == "approve":
        logger.info("Manager approved '%s'", tool_call["name"])
        return {
            "approval_response": "approved",
            "pending_approval": None,
        }

    # Rejected: return a ToolMessage so the model knows the action was blocked
    logger.info("Manager rejected '%s': %s", tool_call["name"], decision)
    return {
        "messages": [
            ToolMessage(
                content=f"Action rejected by manager. Reason: {decision}",
                tool_call_id=tool_call["id"],
            )
        ],
        "approval_response": decision,
        "pending_approval": None,
    }
