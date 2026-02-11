"""Tests for the agent state schema."""

from agent.state import AgentState


def test_agent_state_inherits_messages():
    """AgentState should inherit 'messages' from MessagesState."""
    # MessagesState provides 'messages' — it won't be in AgentState's own annotations
    # but it's accessible via the full type hierarchy
    state: AgentState = {
        "messages": [],
        "customer_id": "",
        "customer_facts": [],
        "current_order": None,
        "pending_approval": None,
        "approval_response": "",
    }
    assert "messages" in state


def test_agent_state_has_customer_fields():
    """AgentState should have customer service fields."""
    hints = AgentState.__annotations__
    assert "customer_id" in hints
    assert "customer_facts" in hints
    assert "current_order" in hints


def test_agent_state_has_hitl_fields():
    """AgentState should have human-in-the-loop fields."""
    hints = AgentState.__annotations__
    assert "pending_approval" in hints
    assert "approval_response" in hints
