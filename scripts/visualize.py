"""Print the Mermaid diagram of the agent graph."""

from agent.graph import graph

if __name__ == "__main__":
    print(graph.get_graph().draw_mermaid())
