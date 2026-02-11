"""Tool: update customer account details (SENSITIVE — requires manager approval)."""

from __future__ import annotations

from langchain_core.tools import tool

# Simulated customer database for demonstration.
_CUSTOMERS = {
    "alice@example.com": {
        "email": "alice@example.com",
        "name": "Alice Johnson",
        "phone": "+1-555-0101",
        "address": "123 Main St, Springfield, IL 62701",
    },
    "bob@example.com": {
        "email": "bob@example.com",
        "name": "Bob Smith",
        "phone": "+1-555-0102",
        "address": "456 Oak Ave, Portland, OR 97201",
    },
}


@tool
def update_account(
    customer_email: str,
    field: str,
    new_value: str,
) -> str:
    """Update a field on a customer's account.

    This is a sensitive action that requires manager approval before execution.
    The agent graph will automatically pause for approval when this tool is called.

    Args:
        customer_email: The customer's email address.
        field: The field to update ('name', 'phone', or 'address').
        new_value: The new value for the field.
    """
    allowed_fields = {"name", "phone", "address"}
    if field not in allowed_fields:
        return f"Cannot update '{field}'. Allowed fields: {', '.join(sorted(allowed_fields))}."

    customer = _CUSTOMERS.get(customer_email)
    if not customer:
        return f"No customer found with email '{customer_email}'."

    old_value = customer[field]
    customer[field] = new_value

    return (
        f"Account updated for {customer_email}: "
        f"{field} changed from '{old_value}' to '{new_value}'."
    )
