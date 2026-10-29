Ref Answer:
30 orders written; unfulfilled > 3 days: ['#1002', '#1006', '#1007', '#1008', '#1012', '#1014', '#1016', '#1019', '#1022','#1025', '#1027']

-------
Q: Which orders are unfulfilled for more than 3 days, and how many days each?
Response: Eleven orders have been unfulfilled for more than 3 days, as of 2026-10-28:

| Order | Days unfulfilled |
|---|---|
| #1016 | 12 |
| #1027 | 11 |
| #1007 | 10 |
| #1014 | 10 |
| #1019 | 10 |
| #1025 | 10 |
| #1002 | 9 |
| #1008 | 9 |
| #1006 | 8 |
| #1012 | 6 |
| #1022 | 6 |

I left out #1005, which is exactly 3 days old, and #1023, which is 1 day old.

Verdict: Right
Reason: Verified from ref answer
-------

Q: How many orders were cancelled this week?
Response: **1 order** was created and cancelled this week (Mon Oct 26 – today, Oct 28): **#1015** (Bilal Ahmed, created Oct 28).

- The data only has creation dates, not cancellation dates. So this counts orders created this week that are now cancelled. Some of the others could have been cancelled this week.
- If you mean the last 7 days (Oct 22–28), the count is **4**: #1001, #1015, #1018 and #1029.
Verdict: correct. Noticed there's no cancelled_at field and answered both meanings of "this week".

------------
When removed "never guess" from system.
Q: Which orders are unfulfilled for more than 3 days, and how many days each?
14 orders are unfulfilled. 
Count is wrong. They are 13 not 14
------------
Q: What is the total revenue of fulfilled orders?
Response: **Total revenue of fulfilled orders: 174,600.** This covers 13 orders. The data has no currency, so the figure is in the store's price units.

| Order | Total |
|---|---|
| #1003 | 7,800 |
| #1004 | 23,400 |
| #1009 | 17,400 |
| #1010 | 15,600 |
| #1011 | 19,200 |
| #1013 | 3,000 |
| #1017 | 2,700 |
| #1020 | 20,400 |
| #1021 | 18,900 |
| #1024 | 9,300 |
| #1026 | 9,600 |
| #1028 | 24,300 |
| #1030 | 3,000 |

I calculated each total as price × qty, summed over the items in the order. The figure excludes shipping, taxes and discounts, because the data doesn't include them.

Verdict: It seems correct
--------------
Q: Which customer has the most open orders?
Response: **Bilal Ahmed** has the most open (unfulfilled) orders, with 4: #1002, #1005, #1022 and #1027.

Next are Hina Raza (3: #1006, #1008, #1023) and Ayesha Khan (3: #1007, #1019, #1025). Usman Tariq has 2 and Sara Malik has 1.

I counted only unfulfilled orders as "open".

Verdict: Correct.

---------------

# Day2

uv run answer_key.py
1. Unfulfilled > 3 days: [('#1016', 12), ('#1027', 11), ('#1007', 10), ('#1014', 10), ('#1019', 10), ('#1025', 10), ('#1002', 9), ('#1008', 9), ('#1006', 8), ('#1012', 6), ('#1022', 6)]
   Total unfulfilled: 13
2. Cancelled since Mon 26 Oct: [('#1001', '2026-10-26'), ('#1015', '2026-10-28'), ('#1029', '2026-10-26')]
3. Fulfilled revenue (PKR): 174600
4. Open orders by customer: [('Bilal Ahmed', 4), ('Hina Raza', 3), ('Ayesha Khan', 3), ('Usman Tariq', 2), ('Sara Malik', 1)]
5. Units sold by SKU (fulfilled): [('SNEAKER-42', 16), ('CAP-RED', 9), ('TSHIRT-BLK-M', 8), ('JEANS-32', 6), ('TSHIRT-WHT-L', 3)]
6. Fulfilled revenue by city: [('Lahore', 72600), ('Multan', 32400), ('Karachi', 29700), ('Faisalabad', 24300), ('Islamabad', 15600)]
## Day 2 results (checked against answer_key.py) — score 6/6

| # | Question | Tool calls | Verdict |
|---|---|---|---|
| Q1 | Unfulfilled > 3 days + total | get_orders(status=unfulfilled) | ✓ 13 total (Day 1 bug fixed via `count`), 11 late, days right. "11" was still counted by the model → fix: older_than_days filter |
| Q2 | Cancelled this week | get_orders(cancelled, date_field=cancelled_at, 26–28 Oct) | ✓ 3 (#1001, #1029, #1015). New cancelled_at field made it answerable |
| Q3 | Revenue of fulfilled orders | order_stats(status=fulfilled) | ✓ PKR 174,600, 13 orders, 42 units — all from SQL |
| Q4 | Customer with most open orders | order_stats(unfulfilled, group_by=customer) | ✓ Bilal Ahmed, 4 orders |
| Q5 | Best-selling SKU | order_stats ×3 (all / fulfilled / unfulfilled) | ✓ SNEAKER-42. Handled ambiguity: by units across all orders TSHIRT-WHT-L leads (27 vs 26), but 6 cancelled + 18 unfulfilled |
| Q6 | City with most revenue | order_stats ×2 (all / fulfilled) | ✓ Lahore either way (72,600 fulfilled / 163,500 all) |
| Bonus | Tell me about #1016 | get_order + an extra get_orders | ✓ items, total 11,700, 12 days. Extra call was unnecessary |

Learnings:
- Code does the maths, model decides what to compute: every number today came from SQL or `count`.
- Model picked order_stats for every total/ranking question without being told which question → tool descriptions work.
- Business definitions are missing: "revenue" and "best-selling" mean fulfilled orders in real life, but the agent starts from all orders (incl. cancelled). Fix: define them in SYSTEM or make fulfilled the default.
- Adding one data field (cancelled_at) turned an unanswerable question into an exact one.
- Watch for wasted tool calls (Bonus question): they cost money and time.
