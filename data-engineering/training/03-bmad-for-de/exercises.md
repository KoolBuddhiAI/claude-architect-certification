# Module 03: Hands-On Exercises

## Exercise 1 — Quick (20 min): Write a Data Contract

**Goal:** Practice the ANALYZE + ARCHITECT output before any code.

**Scenario:** You're building a pipeline to load daily sales data from a CSV export into your warehouse. The CSV has: `order_id`, `customer_email`, `product_name`, `quantity`, `unit_price`, `order_date`.

Write the data contract:

```markdown
## Data Contract: [table name you'd create]

**Business Question:**
What does this data answer?

**Consumers:**
Who will use this and what do they trust?

**Source:**
Where does it come from, how often does it update?

**Target Schema:**
| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| ...    | ...  | ...      | ...   |

**Compliance:**
Any PII or retention concerns?

**Quality Gates:**
Critical (blocks):
- [ ]
Warning (alerts):
- [ ]

**Join Dependencies:**
Does this join with any existing tables? What column?
```

**Reflection:** Notice that this takes 15–20 minutes but prevents at least one misunderstanding that would cost 2–4 hours to fix after the fact.

---

## Exercise 2 — Medium (45 min): Decompose a Pipeline into Waves

**Goal:** Practice the DECOMPOSE phase with a multi-source pipeline.

**Scenario:** You're building a customer 360 data product. It needs:
- Ingest customer data from CRM (Salesforce)
- Ingest order data from e-commerce platform (Shopify)
- Ingest support tickets from Zendesk
- Build `dim_customer` (grain: one row per customer)
- Build `fact_orders` (grain: one row per order)
- Build `fact_support` (grain: one row per ticket)
- Build `customer_360` (joins all three facts to dim_customer)
- Build `agg_customer_value` (summary metrics per customer)

**Task:**
1. List all the tables each story writes to
2. Identify dependency chains
3. Assign to waves (what can run in parallel? what must be sequential?)
4. Identify any stories that share a table and should NOT run in parallel

**Hint:** The `customer_360` and `agg_customer_value` tables both depend on `dim_customer`. Does that mean they must be sequential?

**Draw the wave diagram:**
```
Wave 1 (parallel):

Wave 2 (parallel within wave, sequential after Wave 1):

Wave 3:
```

**Compare against the solution** after completing: all three raw ingestion tasks (CRM, Shopify, Zendesk) can run in Wave 1. `dim_customer`, `fact_orders`, `fact_support` can all run in Wave 2. `customer_360` runs in Wave 3. `agg_customer_value` runs in Wave 4 (depends on `customer_360`).

---

## Exercise 3 — Deep (90 min): Full BMAD Run on a Real Pipeline

**Goal:** Apply all four BMAD phases to a real pipeline from your work.

Choose a pipeline you're planning to build or rebuild. Something that:
- Has at least two source systems
- Has at least one downstream consumer you care about
- Has some quality or trust requirement

**Phase 1 — ANALYZE (20 min):**
Write the requirements doc using the template from the slides. Focus especially on the "join dependencies" and "compliance" sections — those are the ones most likely to surface surprises.

**Phase 2 — ARCHITECT (25 min):**
Draw the lineage map (even on paper). For every column in your target table, trace it back to a source column. Write the quality contract with at least two critical and two warning gates.

**Phase 3 — DECOMPOSE (15 min):**
Break into stories. Check every story touches only one output table. Identify the wave structure.

**Phase 4 — IMPLEMENT prep (30 min):**
For your first agent story, write the full context block you'd give the agent:
- Source schemas (copy the actual DDL if you have it)
- Target schema
- Transformation rules (explicit, not vague)
- Quality contract
- Idempotency requirement
- Any edge cases you know about

**Deliverable:** A folder with four files: `requirements.md`, `lineage-map.md` (or a hand-drawn image), `wave-plan.md`, `story-01-context.md`. This is a real artifact you can bring into your next sprint.
