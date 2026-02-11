# Customer Service Agent

A production-ready Customer Service Agent built with **LangGraph** and **Google Gemini**.

Meet **Sophie** — a friendly, professional support agent who handles orders, processes refunds, searches company policies, and remembers customer preferences across conversations.

## Features

| Feature | Description |
|---------|------------|
| **Stateful Graph** | LangGraph `StateGraph` with typed state, reducers, and conditional edges |
| **Tools** | 4 domain tools: order lookup, policy search, refunds, account updates |
| **Short-term Memory** | PostgreSQL checkpointer for multi-turn conversation persistence |
| **Long-term Memory** | PostgresStore with Gemini semantic search for customer facts |
| **Human-in-the-Loop** | `interrupt()` pauses the graph for manager approval on refunds and account changes |
| **Agentic RAG** | Vector store retrieval over company policies — the agent decides when to search |
| **Streaming** | Real-time token streaming and node-level progress updates |
| **Retry Policies** | Automatic retries on LLM and tool execution nodes |
| **Observability** | Zero-config LangSmith tracing via environment variables |
| **CI/CD** | GitHub Actions with ruff lint + pytest on every push |

## Graph Topology

```
START → respond → [route] → execute → respond → ... → remember → END
                       ↘ review → [route] → execute / respond
```

- **respond**: Invoke Gemini with tools + customer context
- **execute**: Run tool calls (order lookup, policy search, etc.)
- **review**: `interrupt()` → manager approves/rejects refunds and account changes
- **remember**: Extract customer facts → long-term memory store

## Quick Start

```bash
# Clone
git clone https://github.com/Sapphify/langgraph-production-agent.git
cd langgraph-production-agent

# Install
uv sync

# Configure
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY and POSTGRES_URI

# Run tests
uv run pytest tests/ -v

# Start dev server
langgraph dev
```

## Project Structure

```
src/agent/
├── graph.py          # Main graph assembly
├── state.py          # AgentState schema
├── prompts.py        # Sophie's persona
├── settings.py       # Environment config
├── routing.py        # Edge routing logic
├── nodes/
│   ├── respond.py    # Call Gemini
│   ├── execute.py    # Run tools
│   ├── review.py     # HITL approval
│   └── remember.py   # Save memories
├── tools/
│   ├── orders.py     # Order lookup
│   ├── policies.py   # RAG search
│   ├── refunds.py    # Refund processing
│   └── accounts.py   # Account updates
├── memory/
│   ├── short_term.py # Checkpointer
│   └── long_term.py  # Memory store
└── rag/
    ├── store.py      # Vectorstore
    └── loader.py     # Doc ingestion
```

## Version History

| Tag | Description |
|-----|------------|
| `v0.1.0` | Project scaffold |
| `v0.2.0` | Settings + state + prompts |
| `v0.3.0` | Memory infrastructure |
| `v0.4.0` | Tools + policy documents |
| `v0.5.0` | RAG vectorstore + loader |
| `v0.6.0` | Graph nodes |
| `v0.7.0` | Routing + graph assembly |
| `v0.8.0` | Test suite |
| `v1.0.0` | First release |

## Tech Stack

- **LangGraph** — Stateful agent orchestration
- **Google Gemini** — LLM + embeddings
- **PostgreSQL** — Checkpoints + long-term memory + vectorstore
- **uv** — Fast Python package manager
- **pytest** — Testing
- **ruff** — Linting

## License

MIT
