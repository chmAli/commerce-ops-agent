import json

def get_orders(status: str | None = None) -> list[dict]:
    orders = json.load(open("orders.json"))
    return [o for o in orders if status is None or o["status"] == status]

TOOLS = [{
    "name": "get_orders",
    "description": "Return the store's orders, optionally filtered by status. "
                   "Each order has id, customer, status, created_at, fulfilled_at and items.",
    "input_schema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["unfulfilled", "fulfilled", "cancelled"]}
        },
        "required": [],
    },
}]
