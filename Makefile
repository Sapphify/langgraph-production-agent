.PHONY: dev test lint format ingest viz

dev:
	langgraph dev

test:
	uv run pytest tests/ -v

test-unit:
	uv run pytest tests/test_state.py tests/test_routing.py tests/test_tools.py -v

lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/

ingest:
	uv run python scripts/ingest.py

viz:
	uv run python scripts/visualize.py
