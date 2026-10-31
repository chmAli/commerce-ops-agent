import tools


def test_unfulfilled_count():
    assert tools.get_orders(status="unfulfilled")["count"] == 13


def test_late_orders():
    r = tools.get_orders(status="unfulfilled", older_than_days=3)
    assert r["count"] == 11
    assert r["orders"][0]["id"] == "#1016"
    assert r["orders"][0]["age_days"] == 12


def test_fulfilled_revenue():
    [row] = tools.order_stats(status="fulfilled")
    assert (row["orders"], row["units"], row["revenue_pkr"]) == (13, 42, 174600)


def test_order_by_orders():
    rows = tools.order_stats(status="unfulfilled", group_by="customer", order_by="orders")
    assert rows[0]["grp"] == "Bilal Ahmed"
    assert rows[0]["orders"] == 4


def test_bad_order_by_is_ignored():
    rows = tools.order_stats(group_by="customer", order_by="1; DROP TABLE orders")
    assert len(rows) == 6  # fell back to revenue; the query still ran safely


def test_cancelled_this_week():
    r = tools.get_orders(status="cancelled", date_field="cancelled_at", date_from="2026-10-26")
    assert sorted(o["id"] for o in r["orders"]) == ["#1001", "#1015", "#1029"]


def test_missing_order():
    assert "error" in tools.get_order("#9999")