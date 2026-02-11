"""Short-term memory: PostgreSQL checkpointer for conversation persistence.

Each conversation thread is identified by a ``thread_id``. The checkpointer
saves the full agent state after every graph step, enabling:
- Multi-turn conversations that survive process restarts
- Human-in-the-loop interrupt/resume across sessions
- Time-travel debugging (replay from any checkpoint)
"""

from __future__ import annotations

import logging

from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agent.settings import settings

logger = logging.getLogger(__name__)

_checkpointer: AsyncPostgresSaver | MemorySaver | None = None


async def get_checkpointer() -> AsyncPostgresSaver | MemorySaver:
    """Get or create the checkpointer singleton.

    Uses PostgreSQL in production (when ``POSTGRES_URI`` is configured)
    and falls back to in-memory for development.
    """
    global _checkpointer
    if _checkpointer is not None:
        return _checkpointer

    if settings.postgres_uri and "localhost" not in settings.postgres_uri:
        logger.info("Using PostgreSQL checkpointer")
        _checkpointer = AsyncPostgresSaver.from_conn_string(settings.postgres_uri)
        await _checkpointer.setup()
    else:
        logger.info("Using in-memory checkpointer (dev mode)")
        _checkpointer = MemorySaver()

    return _checkpointer
