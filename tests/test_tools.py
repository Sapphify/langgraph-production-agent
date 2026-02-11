"""Tests for customer service tools."""

from agent.tools import SENSITIVE_TOOLS, TOOLS
from agent.tools.accounts import update_account
from agent.tools.orders import lookup_order
from agent.tools.refunds import process_refund


class TestLookupOrder:
    """Test the order lookup tool."""

    def test_find_by_order_id(self):
        result = lookup_order.invoke({"order_id": "ORD-1001"})
        assert "ORD-1001" in result
        assert "Wireless Headphones" in result
        assert "delivered" in result

    def test_find_by_email(self):
        result = lookup_order.invoke({"customer_email": "alice@example.com"})
        assert "ORD-1001" in result
        assert "ORD-1003" in result

    def test_not_found(self):
        result = lookup_order.invoke({"order_id": "ORD-9999"})
        assert "No order found" in result

    def test_missing_params(self):
        result = lookup_order.invoke({"order_id": "", "customer_email": ""})
        assert "provide" in result.lower()


class TestProcessRefund:
    """Test the refund tool."""

    def test_successful_refund(self):
        result = process_refund.invoke({
            "order_id": "ORD-1001",
            "reason": "Defective item",
            "amount": 79.99,
        })
        assert "processed successfully" in result
        assert "$79.99" in result

    def test_refund_full_order(self):
        result = process_refund.invoke({
            "order_id": "ORD-1001",
            "reason": "Changed my mind",
        })
        assert "processed successfully" in result

    def test_refund_order_not_found(self):
        result = process_refund.invoke({
            "order_id": "ORD-9999",
            "reason": "test",
        })
        assert "not found" in result

    def test_refund_exceeds_total(self):
        result = process_refund.invoke({
            "order_id": "ORD-1001",
            "reason": "test",
            "amount": 999.99,
        })
        assert "exceeds" in result


class TestUpdateAccount:
    """Test the account update tool."""

    def test_update_phone(self):
        result = update_account.invoke({
            "customer_email": "alice@example.com",
            "field": "phone",
            "new_value": "+1-555-9999",
        })
        assert "updated" in result.lower()
        assert "phone" in result

    def test_invalid_field(self):
        result = update_account.invoke({
            "customer_email": "alice@example.com",
            "field": "password",
            "new_value": "secret",
        })
        assert "Cannot update" in result

    def test_customer_not_found(self):
        result = update_account.invoke({
            "customer_email": "nobody@example.com",
            "field": "name",
            "new_value": "Nobody",
        })
        assert "No customer found" in result


class TestToolRegistry:
    """Test the tool registry."""

    def test_tools_list_has_all_tools(self):
        tool_names = {t.name for t in TOOLS}
        assert "lookup_order" in tool_names
        assert "search_policies" in tool_names
        assert "process_refund" in tool_names
        assert "update_account" in tool_names

    def test_sensitive_tools_are_subset(self):
        tool_names = {t.name for t in TOOLS}
        assert SENSITIVE_TOOLS.issubset(tool_names)

    def test_sensitive_tools_correct(self):
        assert "process_refund" in SENSITIVE_TOOLS
        assert "update_account" in SENSITIVE_TOOLS
        assert "lookup_order" not in SENSITIVE_TOOLS
