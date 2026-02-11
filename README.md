<div align="center">

# LangGraph Production Agent

**A production-ready Customer Service Agent built with LangGraph and Google Gemini**

[![CI](https://github.com/Sapphify/langgraph-production-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Sapphify/langgraph-production-agent/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-v0.3-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Built by [**Sapphify**](https://sapphify.com) — Custom Technology Solutions

</div>

---

Meet **Sophie** — a stateful AI support agent that handles orders, processes refunds, searches company policies via RAG, and remembers customer preferences across conversations. Built as a reference implementation showcasing LangGraph's core capabilities in a real-world scenario.

## Why This Project

Most LangGraph examples are toy demos. This is a **full production architecture** — typed state, durable memory, human approval workflows, and agentic retrieval — wired together in a clean, maintainable codebase.

Use it as a starting point for your own agents, or as a study reference for LangGraph best practices.

## Key Features

| | Feature | Implementation |
|---|---------|---------------|
| **State** | Typed `AgentState` with reducers | `MessagesState` + custom fields for orders, approvals, customer facts |
| **Tools** | 4 domain tools | Order lookup, policy search (RAG), refund processing, account updates |
| **Short-term Memory** | Conversation persistence | PostgreSQL checkpointer — survives crashes, resumes from last turn |
| **Long-term Memory** | Customer preferences | Semantic search via Gemini embeddings, namespaced per customer |
| **Human-in-the-Loop** | Manager approval flow | `interrupt()` pauses on sensitive ops, `Command(resume=)` continues |
| **Agentic RAG** | Policy retrieval | Agent decides when to search — vectorstore over company docs |
| **Streaming** | Real-time output | Token-level streaming + node progress updates |
| **Reliability** | Retry policies | Auto-retry on LLM (3x) and tool execution (2x) nodes |
| **Observability** | Tracing | Zero-config LangSmith integration via env vars |
| **CI/CD** | Automated checks | GitHub Actions — ruff lint + pytest on every push |

## Architecture

```
START
  │
  v
respond ◄─────────────────────────┐
  │                                │
  ├─[tool calls + sensitive]──► review
  │                              │
  │                    ┌─approved──► execute ──┐
  │                    │                       │
  │                    └─rejected──────────────┤
  │                                            │
  ├─[tool calls, safe]──────► execute ─────────┘
  │
  └─[no tool calls]─────────► remember ──► END
```

| Node | Role | Retry |
|------|------|-------|
| `respond` | Invoke Gemini with tools + customer context | 3x |
| `execute` | Run tool calls via `ToolNode` | 2x |
| `review` | `interrupt()` — manager approves/rejects sensitive operations | — |
| `remember` | Extract customer facts to long-term memory | 2x |

## Quick Start

```bash
# Clone
git clone https://github.com/Sapphify/langgraph-production-agent.git
cd langgraph-production-agent

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Set GOOGLE_API_KEY and POSTGRES_URI in .env

# Run tests
uv run pytest tests/ -v

# Start the LangGraph dev server
langgraph dev
```

> Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

## Project Structure

```
src/agent/
├── graph.py              # Graph assembly — build + compile + export
├── state.py              # AgentState schema (MessagesState + domain fields)
├── prompts.py            # Sophie's persona and system prompt
├── settings.py           # Pydantic settings from .env
├── routing.py            # Conditional edge logic
│
├── nodes/                # Graph nodes (verbs — what the agent does)
│   ├── respond.py        # Call Gemini with tools
│   ├── execute.py        # Run tool calls
│   ├── review.py         # Human-in-the-loop approval
│   └── remember.py       # Save facts to long-term memory
│
├── tools/                # Domain tools (nouns — what the agent works with)
│   ├── orders.py         # Order lookup by ID or email
│   ├── policies.py       # RAG search over company policies
│   ├── refunds.py        # Refund processing (sensitive — triggers HITL)
│   └── accounts.py       # Account updates (sensitive — triggers HITL)
│
├── memory/               # Persistence layer
│   ├── short_term.py     # PostgresSaver checkpointer
│   └── long_term.py      # PostgresStore + Gemini embeddings
│
└── rag/                  # Retrieval-Augmented Generation
    ├── store.py          # Vectorstore setup
    └── loader.py         # Policy document ingestion
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Orchestration | [LangGraph](https://langchain-ai.github.io/langgraph/) |
| LLM + Embeddings | [Google Gemini](https://ai.google.dev/) |
| Persistence | [PostgreSQL](https://www.postgresql.org/) (checkpoints + memory + vectors) |
| Package Manager | [uv](https://docs.astral.sh/uv/) |
| Linting | [ruff](https://docs.astral.sh/ruff/) |
| Testing | [pytest](https://docs.pytest.org/) |
| CI/CD | [GitHub Actions](https://github.com/features/actions) |

## Version History

| Tag | Milestone |
|-----|-----------|
| `v0.1.0` | Project scaffold — pyproject.toml, CI, structure |
| `v0.2.0` | Settings, state schema, agent persona |
| `v0.3.0` | Memory infrastructure — checkpointer + store |
| `v0.4.0` | Domain tools + policy documents |
| `v0.5.0` | RAG vectorstore + document loader |
| `v0.6.0` | Graph nodes — respond, execute, review, remember |
| `v0.7.0` | Routing logic + graph assembly |
| `v0.8.0` | Test suite — unit + integration |
| `v1.0.0` | First release |

## About

This project is developed and maintained by [**Sapphify**](https://sapphify.com) — a technology solutions company delivering custom software development, automation, and digital transformation services worldwide.

- Website: [sapphify.com](https://sapphify.com)
- GitHub: [github.com/Sapphify](https://github.com/Sapphify)
- LinkedIn: [linkedin.com/company/sapphify](https://linkedin.com/company/sapphify)
- Contact: [info@sapphify.com](mailto:info@sapphify.com)

## License

MIT
