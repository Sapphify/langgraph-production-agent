"""Tool registry for the customer service agent.

TOOLS — all tools the agent can call.
SENSITIVE_TOOLS — tool names that require manager approval via human-in-the-loop.
"""

from agent.tools.accounts import update_account
from agent.tools.orders import lookup_order
from agent.tools.policies import search_policies
from agent.tools.refunds import process_refund

TOOLS = [
    lookup_order,
    search_policies,
    process_refund,
    update_account,
]

SENSITIVE_TOOLS: set[str] = {
    "process_refund",
    "update_account",
}
