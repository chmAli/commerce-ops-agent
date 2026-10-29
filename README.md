# commerce-ops-agent

An LLM agent that answers e-commerce operations questions (stuck orders, revenue,
customers) by calling tools over store data instead of guessing.

## Run

    uv sync
    echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
    uv run make_data.py
    uv run --env-file .env agent.py

## Status

Day 1: agent loop with one tool (`get_orders`), fake Shopify-style data.
Next: more tools, SQLite, MCP server, evals.

Day 3: MCP server (server.py), works in Claude Desktop