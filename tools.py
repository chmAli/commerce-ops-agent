import sqlite3

DB = "store.db"
TODAY = "2026-10-28"  # must match TODAY in make_data.py
DATE_FIELDS = {"created_at", "fulfilled_at", "cancelled_at"}


def _query(sql, params=()):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row  # rows come back as dict-like objects
    rows = [dict(r) for r in con.execute(sql, params)]
    con.close()
    return rows


def _where(status=None, date_field="created_at", date_from=None, date_to=None, customer=None):
    """Builds the WHERE clause shared by get_orders and order_stats."""
    if date_field not in DATE_FIELDS:
        date_field = "created_at"
    clauses, params = ["1=1"], []
    if status:
        clauses.append("o.status = ?"); params.append(status)
    if date_from:
        clauses.append(f"o.{date_field} >= ?"); params.append(date_from)
    if date_to:
        clauses.append(f"o.{date_field} <= ?"); params.append(date_to)
    if customer:
        clauses.append("o.customer LIKE ?"); params.append(f"%{customer}%")
    return " AND ".join(clauses), params


def get_orders(status=None, date_field="created_at", date_from=None, date_to=None, customer=None,
               older_than_days=None):
    where, params = _where(status, date_field, date_from, date_to, customer)
    rows = _query(f"""SELECT o.*, CAST(julianday(?) - julianday(o.created_at) AS INTEGER) AS age_days
                      FROM orders o WHERE {where} ORDER BY o.created_at""", [TODAY] + params)
    if older_than_days is not None:
        rows = [r for r in rows if r["age_days"] > older_than_days]
    return {"count": len(rows), "orders": rows}


def get_order(order_id):
    found = _query("SELECT * FROM orders WHERE id = ?", (order_id,))
    if not found:
        return {"error": f"order {order_id} not found"}
    order = found[0]
    order["items"] = _query("SELECT sku, qty, price FROM order_items WHERE order_id = ?", (order_id,))
    order["total_pkr"] = sum(i["qty"] * i["price"] for i in order["items"])
    return order


def get_customer(name):
    found = _query("SELECT * FROM customers WHERE name LIKE ?", (f"%{name}%",))
    if not found:
        return {"error": f"no customer matching {name}"}
    for c in found:
        c["orders"] = _query("SELECT id, status, created_at FROM orders WHERE customer = ?", (c["name"],))
    return found


def order_stats(group_by=None, status=None, date_field="created_at", date_from=None, date_to=None, customer=None):
    group = {"customer": "o.customer", "status": "o.status", "sku": "i.sku", "city": "c.city"}.get(group_by, "'all'")
    where, params = _where(status, date_field, date_from, date_to, customer)
    return _query(f"""SELECT {group} AS grp, COUNT(DISTINCT o.id) AS orders, SUM(i.qty) AS units,
                             SUM(i.qty * i.price) AS revenue_pkr
                      FROM orders o
                      JOIN order_items i ON i.order_id = o.id
                      JOIN customers c ON c.name = o.customer
                      WHERE {where} GROUP BY grp ORDER BY revenue_pkr DESC""", params)


FILTERS = {
    "status": {"type": "string", "enum": ["unfulfilled", "fulfilled", "cancelled"]},
    "date_field": {"type": "string", "enum": ["created_at", "fulfilled_at", "cancelled_at"],
                   "description": "Which date date_from/date_to filter on. Default created_at."},
    "date_from": {"type": "string", "description": "Inclusive start date, YYYY-MM-DD"},
    "date_to": {"type": "string", "description": "Inclusive end date, YYYY-MM-DD"},
    "customer": {"type": "string", "description": "Customer name or part of it"},
}

TOOLS = [
    {"name": "get_orders",
     "description": "List orders matching the filters. Returns an exact count and the orders; each order has "
                    "age_days (whole days since it was created, as of today). Use count and age_days "
                    "instead of counting or doing date maths yourself.",
    "input_schema": {"type": "object",
                     "properties": {**FILTERS,
                                    "older_than_days": {"type": "integer",
                                    "description": "Only orders created more than this many days ago"}},
                    "required": []}},
    {"name": "get_order",
     "description": "Full details of one order, including line items and total in PKR.",
     "input_schema": {"type": "object", "properties": {"order_id": {"type": "string", "description": "e.g. #1016"}},
                      "required": ["order_id"]}},
    {"name": "get_customer",
     "description": "A customer's email and city, plus a list of their orders.",
     "input_schema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
    {"name": "order_stats",
     "description": "Exact totals computed in SQL: number of orders, units and revenue in PKR for orders matching "
                    "the filters, optionally grouped by customer, status, sku or city. Use this for any count, "
                    "sum, ranking or most/least question.",
     "input_schema": {"type": "object",
                      "properties": {"group_by": {"type": "string", "enum": ["customer", "status", "sku", "city"]},
                                     **FILTERS},
                      "required": []}},
]

FUNCTIONS = {"get_orders": get_orders, "get_order": get_order,
             "get_customer": get_customer, "order_stats": order_stats}