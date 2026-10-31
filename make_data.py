import random
import sqlite3
from datetime import date, timedelta

random.seed(7)
TODAY = date(2026, 10, 28)
customers = ["Ayesha Khan", "Bilal Ahmed", "Sara Malik", "Usman Tariq", "Hina Raza", "Omar Farooq"]
cities = {"Ayesha Khan": "Lahore", "Bilal Ahmed": "Karachi", "Sara Malik": "Islamabad",
          "Usman Tariq": "Lahore", "Hina Raza": "Faisalabad", "Omar Farooq": "Multan"}
skus = {"TSHIRT-BLK-M": 1500, "TSHIRT-WHT-L": 1500, "JEANS-32": 4200, "CAP-RED": 900, "SNEAKER-42": 7800}

# Same loop as Day 1, so the same 30 orders come out
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

# New: cancellation dates, from a separate random generator so the orders above don't change
extra = random.Random(11)
for o in orders:
    o["cancelled_at"] = None
    if o["status"] == "cancelled":
        created = date.fromisoformat(o["created_at"])
        o["cancelled_at"] = str(min(created + timedelta(days=extra.randint(0, 4)), TODAY))


# New: write everything into a SQLite database
db = sqlite3.connect("store.db")
db.executescript("""
DROP TABLE IF EXISTS order_items; DROP TABLE IF EXISTS orders; DROP TABLE IF EXISTS customers;
CREATE TABLE customers (name TEXT PRIMARY KEY, email TEXT, city TEXT);
CREATE TABLE orders (id TEXT PRIMARY KEY, customer TEXT REFERENCES customers(name), status TEXT,
                     created_at TEXT, fulfilled_at TEXT, cancelled_at TEXT);
CREATE TABLE order_items (order_id TEXT REFERENCES orders(id), sku TEXT, qty INTEGER, price INTEGER);
""")
db.executemany("INSERT INTO customers VALUES (?, ?, ?)",
               [(n, n.lower().replace(" ", ".") + "@example.com", cities[n]) for n in customers])
db.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
               [(o["id"], o["customer"], o["status"], o["created_at"], o["fulfilled_at"], o["cancelled_at"])
                for o in orders])
db.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?)",
               [(o["id"], it["sku"], it["qty"], it["price"]) for o in orders for it in o["items"]])
db.commit()

n_orders = db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
n_items = db.execute("SELECT COUNT(*) FROM order_items").fetchone()[0]
print(f"store.db written: {n_orders} orders, {n_items} order lines, {len(customers)} customers")