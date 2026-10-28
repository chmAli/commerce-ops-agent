import json, random
from datetime import date, timedelta

random.seed(7)
TODAY = date(2026, 10, 28)
customers = ["Ayesha Khan", "Bilal Ahmed", "Sara Malik", "Usman Tariq", "Hina Raza", "Omar Farooq"]
skus = {"TSHIRT-BLK-M": 1500, "TSHIRT-WHT-L": 1500, "JEANS-32": 4200, "CAP-RED": 900, "SNEAKER-42": 7800}

orders = []

for i in range(1, 31):
    created = TODAY - timedelta(days=random.randint(0, 14))
    status = random.choices(["unfulfilled", "fulfilled", "cancelled"], [0.35, 0.55, 0.10])[0]
    items = [{"sku": s, "qty": random.randint(1, 3), "price": skus[s]}
             for s in random.sample(list(skus), random.randint(1, 3))]
    fulfilled_at = None
    if status == "fulfilled":
        fulfilled_at = str(min(created + timedelta(days=random.randint(0, 3)), TODAY))
    orders.append({"id": f"#{1000 + i}", "customer": random.choice(customers), "status": status,
                   "created_at": str(created), "fulfilled_at": fulfilled_at, "items": items})

json.dump(orders, open("orders.json", "w"), indent=2)
late = [o["id"] for o in orders
        if o["status"] == "unfulfilled" and (TODAY - date.fromisoformat(o["created_at"])).days > 3]
print(f"{len(orders)} orders written; unfulfilled > 3 days: {late}")
