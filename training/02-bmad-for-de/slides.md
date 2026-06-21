---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# Here's What Goes Wrong When You Skip the Plan

*And how the BMAD method fixes it*

*Module 02 · AI-Native Data Engineering*

---

# A familiar disaster

Two engineers, same warehouse, working in parallel.

Engineer A builds a `revenue` column in the `orders` table.
Engineer B builds a `revenue` column in the `order_items` table.

Both are technically correct. Both pass their tests. Both ship.

Three weeks later, Finance notices the numbers don't match.

**Root cause**: two different definitions of "revenue" — and nobody wrote them down before coding started.

AI doesn't fix this problem. At AI speed, it makes it **much worse**.

---

# BMAD is the fix

**Breakthrough Method for Agile AI-Driven Development**

Core thesis:
> "Planning is the multiplier. Code without a plan creates chaos at AI speed."

Originally built for software development. This module adapts it specifically for **data engineering**.

The key innovation: **document sharding** — breaking complex specs into atomic, AI-digestible pieces that prevent hallucination and maintain consistency across the project.

---

# Why Data Engineering Needs BMAD

Data engineering has a unique problem that BMAD solves:

**Multiple agents working on the same warehouse = semantic conflicts**

Example:
- Agent A builds a `revenue` column in `orders` table
- Agent B builds a `revenue` column in `order_items` table
- They use different definitions of "revenue"
- Both are correct in isolation. Together, they create a data trust crisis.

**BMAD forces lineage and dependency planning BEFORE implementation.**

---

# The 4 BMAD Phases for Data Engineering

```
Phase 1: ANALYZE
    Define requirements, data sources, consumers

Phase 2: ARCHITECT
    Data model, lineage map, agent roles, quality contracts

Phase 3: DECOMPOSE
    Stories scoped to disjoint data assets (no conflicts)

Phase 4: IMPLEMENT + GOVERN
    Delegate to agents, gate on quality, document outputs
```

---

# Phase 1: ANALYZE

**Goal**: Understand the full problem before touching any code or schema

**Key questions:**
- What business question does this data answer?
- Who are the data consumers? What do they trust?
- What are the source systems? What are their SLAs?
- What data already exists that this must join with?
- What are the compliance requirements? (PII? Retention?)

**BMAD skill**: `/bmad-product-brief` → captures stakeholder requirements
**BMAD skill**: `/bmad-research` → researches existing data landscape

**Output**: A requirements document that agents can reference throughout implementation.

---

# Phase 1: ANALYZE — Template

```markdown
## Data Product Brief

**Business Question**: What revenue did we earn by product category this month?

**Data Consumers**: Finance team (monthly close), Analytics (ad hoc)
**Trust Requirements**: Finance requires reconciliation to source, <0.1% variance

**Source Systems**:
- Stripe API (transactions) — updated every 6 hours
- Salesforce (product catalog) — updated daily
- Existing `customers` table in warehouse — owned by CRM team

**Compliance**: Stripe data contains payment info — must not store card details

**Existing Joins**: Must join to `customers.customer_id` (UUID, not email)

**SLA**: Available by 6am UTC for morning Finance review
```

---

# Phase 2: ARCHITECT

**Goal**: Design the full data architecture before any agent writes code

**Key decisions:**
- Schema design: what tables, what grain, what joins?
- Lineage: where does each column come from?
- Agent roles: what does each pipeline stage do?
- Quality contracts: what makes this data "trusted"?
- Failure modes: what happens when the source is late?

**BMAD skill**: `/bmad-architecture` → generates architecture document
**BMAD skill**: `/bmad-tech-spec` → lightweight alternative for smaller work

---

# Phase 2: ARCHITECT — Lineage Map

```
Stripe API                 Salesforce
    │                          │
    ▼                          ▼
stripe_transactions      product_catalog
(raw, append-only)       (raw, full-refresh)
    │                          │
    └──────────┬───────────────┘
               ▼
      fact_revenue (grain: transaction)
      Columns:
        transaction_id    ← stripe_transactions.id
        customer_id       ← stripe_transactions.customer (FK → customers)
        product_id        ← stripe_transactions.metadata.product_id
        product_category  ← product_catalog.category
        revenue_usd       ← stripe_transactions.amount / 100
        transaction_date  ← stripe_transactions.created (UTC)
               │
               ▼
      agg_revenue_by_category (grain: category × month)
      Consumer: Finance monthly close
```

**Every column has a documented lineage before any agent writes code.**

---

# Phase 2: ARCHITECT — Agent Roles

```
Ingestion Agent
└── Responsibility: Fetch from Stripe API (paginated)
    Quality gate: no null transaction_id, no duplicate IDs
    Output: raw_stripe_transactions

Transformation Agent
└── Responsibility: Build fact_revenue from raw tables
    Quality gate: row count matches source ±0%, revenue sum reconciles
    Output: fact_revenue

Aggregation Agent
└── Responsibility: Build agg_revenue_by_category
    Quality gate: category totals sum to fact_revenue total
    Output: agg_revenue_by_category

Quality Gate Agent (runs after each stage)
└── Responsibility: Validate, block on critical failures
```

---

# Phase 2: ARCHITECT — Quality Contract

```markdown
## Quality Contract: fact_revenue

**Critical (pipeline blocks if violated):**
- Zero null transaction_id values
- Zero duplicate transaction_id values
- Sum(revenue_usd) must match Stripe API total ± 0.01%
- Zero revenue_usd values < 0 (negatives must be refunds, captured separately)

**Warning (alert, proceed with exclusions):**
- Null product_category allowed (new products not yet in catalog)
- Missing customer_id allowed (guest checkouts)

**SLA:**
- Must complete by 05:30 UTC to enable 06:00 Finance review
```

---

# Phase 3: DECOMPOSE

**Goal**: Break architecture into agent tasks with no shared-state conflicts

**Key rule**: Each story must be scoped to **disjoint data assets**. If two stories touch the same table, they cannot run in parallel.

**BMAD skill**: `/bmad-epics-and-stories` → creates file-scoped, dependency-ordered stories
**BMAD skill**: `/bmad-parallel-plan` → groups stories into conflict-free parallel waves

---

# Phase 3: DECOMPOSE — Story Example

```markdown
## Story: Build fact_revenue transformation

**Agent**: Transformation Agent
**Input**: raw_stripe_transactions, product_catalog, customers
**Output**: fact_revenue table
**Touches**: ONLY fact_revenue (no other tables)

**Acceptance criteria:**
- [ ] All columns in data contract present with correct types
- [ ] Quality gate passes: zero nulls on transaction_id
- [ ] Quality gate passes: revenue sum matches raw source ± 0.01%
- [ ] Transformation is idempotent (can re-run without duplication)
- [ ] dbt tests pass for not_null, unique, and accepted_values

**Agent receives**: full data contract, lineage map, source schemas
**Agent must NOT touch**: agg_revenue_by_category (separate story)
```

---

# Phase 3: DECOMPOSE — Parallel Waves

```
Wave 1 (parallel — no conflicts):
├── Story A: Build raw_stripe_transactions ingestion
└── Story B: Refresh product_catalog from Salesforce

Wave 2 (depends on Wave 1):
└── Story C: Build fact_revenue (needs Wave 1 outputs)

Wave 3 (depends on Wave 2):
└── Story D: Build agg_revenue_by_category (needs fact_revenue)

Wave 4 (depends on Wave 3):
└── Story E: Finance reconciliation report (needs aggregation)
```

Agents in the same wave can run in parallel without conflicts.
Agents in different waves must wait for upstream dependencies.

---

# Phase 4: IMPLEMENT + GOVERN

**Goal**: Delegate to agents with complete context; review every output; govern in production

**Implementation**:
- Each story becomes an agent task with the full data contract as context
- Agent generates code, tests, and documentation
- Human reviews against quality contract before merging

**Governance**:
- All agent outputs go through PR review
- Quality gate agent runs on every deploy
- Data catalog auto-updated from agent-generated lineage
- Anomaly alerts configured from quality thresholds

---

# Phase 4: GOVERN — The Review Checklist

Before merging any agent-generated pipeline:

```
□ Schema matches the data contract exactly
□ All quality gate checks implemented
□ Transformation is idempotent
□ Nulls handled per quality contract (critical vs warning)
□ No hardcoded credentials or environment assumptions
□ dbt tests (or equivalent) present and passing
□ Data lineage documented in data catalog
□ Rollback path exists for schema changes
□ SLA timing validated in staging environment
```

---

# BMAD Skill Reference for Data Engineers

| Skill | When to Use |
|---|---|
| `/bmad-init` | Start a new data product |
| `/bmad-product-brief` | Capture stakeholder requirements |
| `/bmad-architecture` | Design full data architecture |
| `/bmad-epics-and-stories` | Decompose into agent tasks |
| `/bmad-parallel-plan` | Find conflict-free parallel waves |
| `/bmad-investigate` | Debug production data issues |
| `/bmad-document-project` | Analyze existing legacy pipelines |
| `/bmad-correct-course` | Handle mid-sprint scope changes |

---

# Module 02 — Key Takeaways

- **BMAD = Plan → Architect → Decompose → Implement → Govern**
- **Lineage mapping before coding** prevents semantic conflicts in multi-agent pipelines
- **Quality contracts** are designed by you, enforced by agents
- **Disjoint story scoping** enables safe parallelization
- **Review checklists** replace trust in agent output

**Next: Module 03 — Workflow Transformation Maps**

---

# Worksheet: Apply BMAD to Your Work

Take a real data engineering task you've done recently and work through:

1. **ANALYZE**: Write the business question and stakeholder requirements (10 min)
2. **ARCHITECT**: Draw the lineage map for 3 key columns (15 min)
3. **ARCHITECT**: Define 3 critical quality gates for the output (10 min)
4. **DECOMPOSE**: Break into 3 stories with disjoint data asset scope (15 min)
5. **IMPLEMENT**: Which stories could run in parallel? Which have dependencies? (5 min)

Total time: ~55 minutes. This is faster than writing the code — and sets agents up to succeed.
