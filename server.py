from typing import Literal

from mcp.server.mcpserver import MCPServer

import tools

mcp = MCPServer("commerce-ops", version="0.1.0")

Status = Literal["unfulfilled", "fulfilled", "cancelled"]
DateField = Literal["created_at", "fulfilled_at", "cancelled_at"]


@mcp.tool()
def get_orders(status: Status | None = None, date_field: DateField = "created_at",
               date_from: str | None = None, date_to: str | None = None,
               customer: str | None = None, older_than_days: int | None = None):
    """List orders matching the filters. Returns an exact count and the orders; each order has
    age_days (whole days since it was created). Dates are YYYY-MM-DD, inclusive.
    older_than_days keeps only orders created more than that many days ago.
    Use count and age_days instead of counting or doing date maths yourself."""
    return tools.get_orders(status, date_field, date_from, date_to, customer, older_than_days)


@mcp.tool()
def get_order(order_id: str):
    """Full details of one order (e.g. #1016), including line items and total in PKR."""
    return tools.get_order(order_id)


@mcp.tool()
def get_customer(name: str):
    """A customer's email and city, plus a list of their orders. Partial names work."""
    return tools.get_customer(name)


@mcp.tool()
def order_stats(group_by: Literal["customer", "status", "sku", "city"] | None = None,
                status: Status | None = None, date_field: DateField = "created_at",
                date_from: str | None = None, date_to: str | None = None, customer: str | None = None,
                order_by: Literal["orders", "units", "revenue"] = "revenue"):
    """Exact totals computed in SQL: number of orders, units and revenue in PKR for orders
    matching the filters, optionally grouped. Use this for any count, sum, ranking or
    most/least question. Revenue normally means fulfilled orders."""
    return tools.order_stats(group_by, status, date_field, date_from, date_to, customer, order_by)


if __name__ == "__main__":
    mcp.run(transport="stdio")
