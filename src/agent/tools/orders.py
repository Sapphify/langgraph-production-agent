"""Tool: look up customer orders."""

from __future__ import annotations

from langchain_core.tools import tool

# Simulated order database for demonstration.
# In production, this would query a real database or API.
_ORDERS = {
    "ORD-1001": {
        "id": "ORD-1001",
        "customer_email": "alice@example.com",
        "items": [{"name": "Wireless Headphones", "qty": 1, "price": 79.99}],
        "total": 79.99,
        "status": "delivered",
        "date": "2026-01-15",
    },
    "ORD-1002": {
        "id": "ORD-1002",
        "customer_email": "bob@example.com",
        "items": [
            {"name": "USB-C Hub", "qty": 1, "price": 49.99},
            {"name": "Laptop Stand", "qty": 1, "price": 34.99},
        ],
        "total": 84.98,
        "status": "shipped",
        "date": "2026-02-01",
        "tracking": "TRK-98765",
    },
    "ORD-1003": {
        "id": "ORD-1003",
        "customer_email": "alice@example.com",
        "items": [{"name": "Mechanical Keyboard", "qty": 1, "price": 129.99}],
        "total": 129.99,
        "status": "processing",
        "date": "2026-02-10",
    },
}


@tool
def lookup_order(order_id: str = "", customer_email: str = "") -> str:
    """Look up an order by order ID or customer email address.

    Provide either an order_id (e.g. 'ORD-1001') or a customer_email to
    find matching orders. Returns order details including items, status,
    and total.
    """
    if order_id:
        order = _ORDERS.get(order_id.upper())
        if order:
            return _format_order(order)
        return f"No order found with ID '{order_id}'."

    if customer_email:
        matches = [o for o in _ORDERS.values() if o["customer_email"] == customer_email]
        if matches:
            return "\n\n---\n\n".join(_format_order(o) for o in matches)
        return f"No orders found for '{customer_email}'."

    return "Please provide either an order_id or customer_email."


def _format_order(order: dict) -> str:
    items = ", ".join(f"{i['name']} (x{i['qty']})" for i in order["items"])
    lines = [
        f"Order: {order['id']}",
        f"Date: {order['date']}",
        f"Items: {items}",
        f"Total: ${order['total']:.2f}",
        f"Status: {order['status']}",
    ]
    if "tracking" in order:
        lines.append(f"Tracking: {order['tracking']}")
    return "\n".join(lines)
