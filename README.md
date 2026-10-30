# commerce-ops-agent

An LLM agent that answers e-commerce operations questions (stuck orders, revenue,
customers) by calling tools over store data instead of guessing.

## Run

    uv sync
    echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
    uv run make_data.py
    uv run --env-file .env agent.py

## Evals

    uv run --env-file .env pytest evals -v

20 cases with answers computed directly from the database; each checks the facts in the answer and, for some, which tool the agent used.

## Status

- Day 1: agent loop from raw API calls, one tool, fake Shopify-style orders.
- Day 2: SQLite and four tools; counts, totals and dates are computed in SQL, not by the model.
- Day 3: MCP server (`server.py`), works in Claude Desktop.
- Day 4: eval suite (20 cases, pytest), score 20/20; business rules in the system prompt, `order_by` for `order_stats`.
