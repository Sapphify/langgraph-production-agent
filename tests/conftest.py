"""Shared test fixtures.

All tests use in-memory backends — no PostgreSQL or API keys needed.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from agent.state import AgentState


@pytest.fixture
def sample_state() -> AgentState:
    """Minimal valid AgentState for testing."""
    return {
        "messages": [HumanMessage(content="Hi, I need help with my order.")],
        "customer_id": "test-customer",
        "customer_facts": [],
        "current_order": None,
        "pending_approval": None,
        "approval_response": "",
    }


@pytest.fixture
def ai_message_with_tool_call():
    """AIMessage that contains a tool call."""
    return AIMessage(
        content="",
        tool_calls=[{
            "name": "lookup_order",
            "args": {"order_id": "ORD-1001"},
            "id": "call_001",
        }],
    )


@pytest.fixture
def ai_message_with_sensitive_tool():
    """AIMessage that contains a sensitive tool call (refund)."""
    return AIMessage(
        content="",
        tool_calls=[{
            "name": "process_refund",
            "args": {"order_id": "ORD-1001", "reason": "Defective item", "amount": 79.99},
            "id": "call_002",
        }],
    )


@pytest.fixture
def ai_message_final():
    """AIMessage with no tool calls (final answer)."""
    return AIMessage(content="Your refund has been processed! 😊")


@pytest.fixture
def mock_llm():
    """Mock ChatGoogleGenerativeAI for testing nodes without API calls."""
    mock = AsyncMock()
    mock.ainvoke.return_value = AIMessage(content="I'd be happy to help! 😊")
    return mock
