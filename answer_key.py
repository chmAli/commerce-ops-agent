import sqlite3

TODAY = "2026-10-28"
db = sqlite3.connect("store.db")

def q(sql, *params):
    return db.execute(sql, params).fetchall()

print("1. Unfulfilled > 3 days:", q("""SELECT id, CAST(julianday(?) - julianday(created_at) AS INTEGER) AS days
    FROM orders WHERE status = 'unfulfilled' AND julianday(?) - julianday(created_at) > 3
    ORDER BY days DESC""", TODAY, TODAY))
print("   Total unfulfilled:", q("SELECT COUNT(*) FROM orders WHERE status = 'unfulfilled'")[0][0])
print("2. Cancelled since Mon 26 Oct:", q("SELECT id, cancelled_at FROM orders WHERE cancelled_at >= '2026-10-26'"))
print("3. Fulfilled revenue (PKR):", q("""SELECT SUM(i.qty * i.price) FROM orders o
    JOIN order_items i ON i.order_id = o.id WHERE o.status = 'fulfilled'""")[0][0])
print("4. Open orders by customer:", q("""SELECT customer, COUNT(*) AS n FROM orders
    WHERE status = 'unfulfilled' GROUP BY customer ORDER BY n DESC"""))
print("5. Units sold by SKU (fulfilled):", q("""SELECT i.sku, SUM(i.qty) AS units FROM orders o
    JOIN order_items i ON i.order_id = o.id WHERE o.status = 'fulfilled' GROUP BY i.sku ORDER BY units DESC"""))
print("6. Fulfilled revenue by city:", q("""SELECT c.city, SUM(i.qty * i.price) AS revenue FROM orders o
    JOIN order_items i ON i.order_id = o.id JOIN customers c ON c.name = o.customer
    WHERE o.status = 'fulfilled' GROUP BY c.city ORDER BY revenue DESC"""))