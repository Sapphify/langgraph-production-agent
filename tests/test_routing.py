"""Tests for edge routing logic."""

from langchain_core.messages import AIMessage, HumanMessage

from agent.routing import route_after_respond, route_after_review


class TestRouteAfterRespond:
    """Test the main routing decision after the model responds."""

    def test_routes_to_execute_for_safe_tool(self, sample_state, ai_message_with_tool_call):
        """Non-sensitive tool calls go directly to execute."""
        sample_state["messages"] = [ai_message_with_tool_call]
        assert route_after_respond(sample_state) == "execute"

    def test_routes_to_review_for_sensitive_tool(
        self, sample_state, ai_message_with_sensitive_tool
    ):
        """Sensitive tool calls (refund, account update) go to review."""
        sample_state["messages"] = [ai_message_with_sensitive_tool]
        assert route_after_respond(sample_state) == "review"

    def test_routes_to_remember_for_final_answer(self, sample_state, ai_message_final):
        """Messages without tool calls go to remember (then END)."""
        sample_state["messages"] = [ai_message_final]
        assert route_after_respond(sample_state) == "remember"

    def test_routes_to_remember_for_human_message(self, sample_state):
        """Non-AI messages default to remember."""
        sample_state["messages"] = [HumanMessage(content="thanks")]
        assert route_after_respond(sample_state) == "remember"

    def test_routes_to_review_for_account_update(self, sample_state):
        """update_account is also a sensitive tool."""
        msg = AIMessage(
            content="",
            tool_calls=[{
                "name": "update_account",
                "args": {
                    "customer_email": "alice@example.com",
                    "field": "phone",
                    "new_value": "+1-555-9999",
                },
                "id": "call_003",
            }],
        )
        sample_state["messages"] = [msg]
        assert route_after_respond(sample_state) == "review"


class TestRouteAfterReview:
    """Test routing after human review."""

    def test_routes_to_execute_when_approved(self, sample_state):
        """Approved actions proceed to tool execution."""
        sample_state["approval_response"] = "approved"
        assert route_after_review(sample_state) == "execute"

    def test_routes_to_respond_when_rejected(self, sample_state):
        """Rejected actions go back to the model."""
        sample_state["approval_response"] = "reject: customer not eligible"
        assert route_after_review(sample_state) == "respond"

    def test_routes_to_respond_when_empty(self, sample_state):
        """Empty approval response defaults to respond."""
        sample_state["approval_response"] = ""
        assert route_after_review(sample_state) == "respond"
