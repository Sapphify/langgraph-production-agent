"""Node: execute tool calls from the model response.

Uses LangGraph's built-in ToolNode which automatically:
1. Reads tool_calls from the last AIMessage
2. Executes each tool with the provided arguments
3. Returns ToolMessage results back to the state
"""

from langgraph.prebuilt import ToolNode

from agent.tools import TOOLS

run_tools = ToolNode(tools=TOOLS)
