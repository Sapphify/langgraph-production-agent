"""Node: call the LLM (Sophie responds to the customer).

This is the core agentic loop node. It invokes Gemini with the full
conversation history, customer context from long-term memory, and all
available tools bound. The model decides whether to call a tool or
provide a final answer.
"""

from __future__ import annotations

import logging

from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from agent.prompts import build_system_prompt
from agent.settings import settings
from agent.state import AgentState
from agent.tools import TOOLS

logger = logging.getLogger(__name__)


async def call_model(state: AgentState) -> dict:
    """Invoke Gemini with tools and the current conversation."""
    model = ChatGoogleGenerativeAI(
        model=settings.model_name,
        temperature=settings.temperature,
        google_api_key=settings.google_api_key,
    ).bind_tools(TOOLS)

    system_msg = SystemMessage(
        content=build_system_prompt(state.get("customer_facts"))
    )
    messages = [system_msg] + state["messages"]

    logger.info("Sophie is thinking... (%d messages in context)", len(messages))
    response = await model.ainvoke(messages)

    return {"messages": [response]}
