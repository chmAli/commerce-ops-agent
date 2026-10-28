import json

def get_orders(status: str | None = None) -> list[dict]:
    orders = json.load(open("orders.json"))
    return [o for o in orders if status is None or o["status"] == status]

TOOLS = [{
    "name": "get_orders",
    "description": "Get data",
    "input_schema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["unfulfilled", "fulfilled", "cancelled"]}
        },
        "required": [],
    },
}]
