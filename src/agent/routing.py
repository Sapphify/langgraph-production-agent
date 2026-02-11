"""Edge routing: conditional logic that controls the graph flow.

Two routing functions determine what happens after:
1. The model responds (tool calls? sensitive? final answer?)
2. A human reviews a sensitive action (approved? rejected?)
"""

from __future__ import annotations

from typing import Literal

from langchain_core.messages import AIMessage

from agent.state import AgentState
from agent.tools import SENSITIVE_TOOLS


def route_after_respond(
    state: AgentState,
) -> Literal["review", "execute", "remember"]:
    """Decide what happens after the model (Sophie) responds.

    - Tool calls with sensitive tools → manager review
    - Tool calls, all safe           → execute tools
    - No tool calls (final answer)   → save memory and end
    """
    last_message = state["messages"][-1]

    if not isinstance(last_message, AIMessage):
        return "remember"

    if not last_message.tool_calls:
        return "remember"

    tool_names = {tc["name"] for tc in last_message.tool_calls}

    if tool_names & SENSITIVE_TOOLS:
        return "review"

    return "execute"


def route_after_review(
    state: AgentState,
) -> Literal["execute", "respond"]:
    """Decide what happens after the manager reviews a sensitive action.

    - Approved → execute the tool
    - Rejected → back to Sophie (she received a rejection ToolMessage)
    """
    if state.get("approval_response") == "approved":
        return "execute"

    return "respond"
