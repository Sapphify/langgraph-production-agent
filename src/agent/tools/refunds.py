"""Tool: process customer refunds (SENSITIVE — requires manager approval)."""

from __future__ import annotations

from langchain_core.tools import tool

# Simulated refund log for demonstration.
_processed_refunds: list[dict] = []


@tool
def process_refund(order_id: str, reason: str, amount: float | None = None) -> str:
    """Process a refund for a customer order.

    This is a sensitive action that requires manager approval before execution.
    The agent graph will automatically pause for approval when this tool is called.

    Args:
        order_id: The order ID to refund (e.g. 'ORD-1001').
        reason: Brief explanation for the refund.
        amount: Refund amount in USD. If not provided, the full order total is refunded.
    """
    from agent.tools.orders import _ORDERS

    order = _ORDERS.get(order_id.upper())
    if not order:
        return f"Cannot process refund: order '{order_id}' not found."

    refund_amount = amount if amount is not None else order["total"]

    if refund_amount > order["total"]:
        return f"Refund amount ${refund_amount:.2f} exceeds order total ${order['total']:.2f}."

    refund = {
        "order_id": order_id.upper(),
        "amount": refund_amount,
        "reason": reason,
        "status": "processed",
    }
    _processed_refunds.append(refund)

    return (
        f"Refund of ${refund_amount:.2f} processed successfully for order {order_id}. "
        f"Reason: {reason}. The customer will receive the refund within 5-7 business days."
    )
