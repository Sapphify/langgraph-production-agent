"""Node: extract and persist customer facts to long-term memory.

Runs after the model produces a final answer (no more tool calls).
Uses a lightweight Gemini call to identify any new facts about the
customer worth remembering for future conversations.

This is how the agent builds personalized context over time:
- "Customer prefers email communication"
- "Customer had an issue with order ORD-1001 (resolved)"
- "Customer lives in Springfield, IL"
"""

from __future__ import annotations

import json
import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from agent.memory.long_term import get_store
from agent.settings import settings
from agent.state import AgentState

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = """\
Analyze the conversation below and extract any new facts about the customer \
that would be useful to remember for future interactions.

Return a JSON array of short strings. If there's nothing new, return [].

Examples of useful facts:
- "Prefers express shipping"
- "Had a defective keyboard replaced (Feb 2026)"
- "Email: alice@example.com"
- "Frustrated about delayed order ORD-1003"

Conversation:
"""


async def save_memory(state: AgentState) -> dict:
    """Extract customer facts from the conversation and store them."""
    messages = state["messages"]
    if len(messages) < 2:
        return {}

    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        google_api_key=settings.google_api_key,
    )

    # Take the last few messages for extraction
    recent = messages[-6:] if len(messages) > 6 else messages
    conversation_text = "\n".join(
        f"{m.type}: {m.content}" for m in recent if hasattr(m, "content") and m.content
    )

    response = await model.ainvoke([
        SystemMessage(content=EXTRACTION_PROMPT),
        HumanMessage(content=conversation_text),
    ])

    try:
        facts = json.loads(response.content)
    except (json.JSONDecodeError, TypeError):
        facts = []

    if not facts:
        return {}

    store = get_store()
    customer_id = state.get("customer_id", "default")

    for fact in facts:
        key = f"fact_{abs(hash(fact)) % 10**8}"
        store.put(
            namespace=(customer_id, "facts"),
            key=key,
            value={"text": fact},
        )
        logger.info("Stored fact for %s: %s", customer_id, fact)

    return {}
