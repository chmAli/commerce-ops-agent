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

## Day 2 wrap-up — Q1 v2

- Added `older_than_days` to get_orders. Calling get_orders(status=unfulfilled, older_than_days=3) returns `count: 11` → the "11 late" number now comes from code, not the model.

## Day 3 — MCP server

- `server.py` publishes the same 4 functions from tools.py over MCP (stdio). Schemas come from type hints + docstrings (`Literal` → enum).
- mcp 2.x renamed FastMCP → MCPServer (`from mcp.server.mcpserver import MCPServer`, `run(transport="stdio")`). Lesson: read the whole error; the fix was in it.
- DB path built from `__file__` so the server works whatever folder it's started from.
- MCP Inspector: order_stats with no filters → 30 orders, 107 units, PKR 352,800 (all statuses). Correct.
- Claude Desktop launches server.py itself as a child process at app start; one process serves every call; restart the app after code changes.
- Verified through MCP: get_orders(unfulfilled, older_than_days=3) → count 11 ✓; order_stats(unfulfilled, group_by=customer) → Bilal Ahmed 4 ✓.
- Finding: order_stats always sorts by revenue, so for "most orders" Bilal comes 3rd in the list and the model must re-rank → add `order_by`.
- Rule: never print() to stdout in a stdio server; use stderr / logging.

## Day 4 — evals (baseline, 30 Oct)

- Built `evals/`: 20 cases in `cases.py` (question + facts the answer must contain + expected tool), pytest runner in `test_agent.py`. Run: `uv run --env-file .env pytest evals -v` (~84 s, a few cents).
- Agent changes: `ask()` records tool calls in `trace` (so tests can check which tool was used) and stops after `max_steps=10` (no endless tool loops).
- **Baseline: 20/20 passed.**

What 20/20 really means:
- `total_revenue` ("What is our total revenue?") was expected to fail and passed. Most likely the answer mentions both 352,800 (all orders) and 174,600 (fulfilled), and a "must contain" check passes as long as the right number appears somewhere. The test is too lenient, not proof the agent knows the business rule. Check with: `pytest evals -v -s -k total_revenue`.
- A perfect score means the eval set is too easy to find problems. Useful evals include cases that fail. Next: harder cases (ambiguous questions, multi-step questions, questions the data can't answer) and "must_not" checks.
- One run isn't enough: the model isn't deterministic, so run the suite 2–3 times before trusting a score.

Lesson: an eval only measures what its checks look at. Write checks that would fail on the wrong answer, not just pass on the right one.
- Checked `total_revenue` with `-s`: 3 tool calls — order_stats(group_by=status) [already contained fulfilled = 174,600], then order_stats({}) [352,800 all orders], then order_stats(status=fulfilled) [174,600 again]. It fetched both numbers to cover both meanings; the third call was redundant (same data as the first). Cost: each tool call is one more model round trip (time + money). Expect the business rule to cut this to 1 call → add a "max tool calls" check to the eval.

## Day 4 part 3 — improve and re-measure (31 Oct)

Changes: business rules in SYSTEM ("revenue / sales / best-selling = fulfilled orders", "open = unfulfilled", "week starts Monday"); `order_by` (orders / units / revenue) on order_stats, in tools.py, TOOLS schema and server.py, mapped through an allowlist dict so model text never goes into SQL.

**Baseline 20/20 → after changes 20/20.** No case changed, nothing got worse. Run time 84 s → 74 s.

What this tells me:
- The score couldn't move, because the baseline was already 20/20 and the checks are lenient. The eval can't show the improvement it was built to measure.
- `total_revenue` passed before the business rule only because the answer contained both numbers. To see the real effect, re-check its tool calls with `-s -k total_revenue` (baseline: 3 calls).
- The ~10 s faster run hints at fewer tool calls overall, but one run isn't proof; the model isn't deterministic.
- Next: make the eval able to fail — a `must_not` check (e.g. total_revenue must not contain 352800), a max-tool-calls check, and harder cases (ambiguous, multi-step, unanswerable). Then run the suite 2–3 times.
