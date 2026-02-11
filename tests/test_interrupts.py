"""Integration tests for human-in-the-loop interrupt/resume flow.

These tests demonstrate the full HITL lifecycle:
1. Customer requests a refund
2. Agent calls process_refund (sensitive tool)
3. Graph pauses at human_review with interrupt()
4. Manager approves/rejects
5. Graph resumes via Command(resume=...)
"""

import pytest
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from agent.graph import build_graph


@pytest.fixture
def test_graph():
    """Compile a fresh graph with in-memory checkpointer for testing."""
    builder = build_graph()
    return builder.compile(checkpointer=MemorySaver())


@pytest.mark.skip(reason="Requires Gemini API key — run locally with GOOGLE_API_KEY set")
class TestHumanInTheLoop:
    """Full interrupt/resume lifecycle tests."""

    @pytest.mark.asyncio
    async def test_refund_approval_flow(self, test_graph):
        """Refund request should pause for approval, then execute on approve."""
        config = {"configurable": {"thread_id": "hitl-test-1"}}

        # Customer asks for a refund — the model should call process_refund
        result = await test_graph.ainvoke(
            {
                "messages": [
                    HumanMessage(
                        content="I want a refund for order ORD-1001, "
                        "the headphones are defective."
                    )
                ],
                "customer_id": "alice",
                "customer_facts": [],
                "current_order": None,
                "pending_approval": None,
                "approval_response": "",
            },
            config=config,
        )

        # The graph should have paused at the review node
        state = test_graph.get_state(config)
        assert state.next  # There should be a next node (review)

        # Manager approves
        result = await test_graph.ainvoke(
            Command(resume="approve"),
            config=config,
        )

        # The refund should have been processed
        messages = result["messages"]
        assert any("processed" in str(m.content).lower() for m in messages)
