"""Integration tests for the full agent graph.

These tests require a Gemini API key. Skip in CI.
"""


from langgraph.checkpoint.memory import MemorySaver

from agent.graph import build_graph, graph


def test_graph_compiles():
    """The graph should compile without errors."""
    assert graph is not None


def test_graph_has_expected_nodes():
    """The compiled graph should have all 4 nodes."""
    node_names = set(graph.get_graph().nodes.keys())
    # __start__ and __end__ are always present
    assert "respond" in node_names
    assert "execute" in node_names
    assert "review" in node_names
    assert "remember" in node_names


def test_graph_renders_mermaid():
    """The graph should render a valid Mermaid diagram."""
    mermaid = graph.get_graph().draw_mermaid()
    assert "respond" in mermaid
    assert "execute" in mermaid
    assert "review" in mermaid
    assert "remember" in mermaid


def test_build_graph_accepts_custom_checkpointer():
    """build_graph should be compilable with a custom checkpointer."""
    builder = build_graph()
    compiled = builder.compile(checkpointer=MemorySaver())
    assert compiled is not None
