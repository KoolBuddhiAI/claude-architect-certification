# Module 02: BMAD for Data Engineering — Reading Guide

## Why Methodology Matters More When You're Fast

Here's the counterintuitive truth about AI-accelerated development: the faster you can execute, the more important it is to plan well.

A human writing a pipeline makes thousands of small decisions as they code — "should this column be nullable?", "what happens if this join produces duplicate rows?" — and those micro-decisions embed judgment into the code.

An agent following a spec makes the decisions the spec implies. If the spec is ambiguous, the agent makes its best guess, and that guess might be consistent within its own pipeline but inconsistent with the pipeline another agent wrote last week.

BMAD solves this by making the critical decisions explicit before execution starts.

---

## Phase 1: ANALYZE — The Questions That Save Hours Later

The ANALYZE phase is the one engineers most often want to skip. It feels like overhead. It isn't.

The questions you're answering in ANALYZE:
1. **What business question does this data answer?** (Prevents building the wrong thing)
2. **Who trusts this data, and what would break their trust?** (Defines your quality bar)
3. **What does this need to join with?** (Prevents semantic conflicts with existing data)
4. **What compliance constraints apply?** (PII, retention, residency)

**The join question is the most commonly skipped and most often regretted.** If you're building a `revenue` column, and the warehouse already has a `revenue` column in three other tables, you need to know: are they the same definition? If not, document the difference before your new one becomes a fourth inconsistent definition.

**Time investment:** 20–40 minutes. Time saved: hours of debugging semantic inconsistencies.

---

## Phase 2: ARCHITECT — The Lineage Map Is the Deliverable

The output of the ARCHITECT phase is a lineage map — not code, not even pseudocode. A lineage map that shows:

- Every source system contributing to the output
- Every intermediate table
- For every column in the final output: what source column it comes from, what transformation was applied

**Why this matters for agents:** When you give an agent a task with a lineage map, it knows exactly what to build. When you give it a vague description, it infers. Inference at AI speed creates inconsistencies at AI scale.

**The quality contract is part of the ARCHITECT phase.** Don't think of quality as something you add at the end. Define it here:
- What does "zero defects" mean for this dataset? (Critical gates)
- What level of badness is acceptable with a warning? (Warning gates)
- What are you willing to let through as informational? (Info)

These three levels map directly to what the quality agent will block, alert on, and log.

---

## Phase 3: DECOMPOSE — Disjoint Assets Are the Rule

The DECOMPOSE phase is where you prevent the revenue-column disaster.

**The rule:** Each story (agent task) must touch only one data asset. If two stories need to write to the same table, they cannot run in parallel. They must be ordered, with the first completing and validating before the second starts.

This is not bureaucracy — it's the same principle as database transactions, applied to your agent orchestration.

**How to check your decomposition:**
- List every table each story writes to
- If two stories in the same wave share a table → move one to the next wave
- If the dependency goes both ways → you have a design problem, not a sequencing problem

**Parallel waves in practice:**

| Wave | Stories | Can parallelize? |
|---|---|---|
| Wave 1 | `ingest_stripe`, `refresh_catalog` | Yes — different tables |
| Wave 2 | `build_fact_revenue` | No — depends on Wave 1 |
| Wave 3 | `build_agg_revenue` | No — depends on Wave 2 |

Wave 1 runs in parallel. Waves 2 and 3 are sequential. The critical path is the chain, not each wave.

---

## Phase 4: IMPLEMENT — Context Is Everything

When you delegate a story to an agent, the agent's quality is directly proportional to the context you provide.

An agent that receives: *"Build the revenue pipeline"* will hallucinate details.

An agent that receives: *"Build `fact_revenue` from `raw_stripe_transactions` (schema attached) and `product_catalog` (schema attached). Revenue is `amount_cents / 100` converted to USD using rate 1.0 for USD, 1.08 for EUR. NULL `product_id` is allowed (guest purchases, set category to 'unassigned'). See quality contract (attached). The transformation must be idempotent — re-runs must not duplicate rows."* will produce something you can actually review and merge.

The time you spend writing context saves you review cycles.

**The review checklist (memorise this):**

1. Does the schema exactly match the data contract?
2. Are nulls handled per the quality contract (not assumed)?
3. Is the transformation idempotent?
4. Is there a quality gate check for every critical threshold?
5. Are there dbt tests (or equivalent) that will catch regressions?
6. Is the lineage documented (even a comment in the model)?

If any answer is "no," send it back before merging. Always.

---

## The BMAD Slash Commands

Install BMAD for Claude Code: `github.com/aj-geddes/claude-code-bmad-skills`

Key commands for data engineers:

```
/bmad-init                → Start a new data product (sets up workspace)
/bmad-product-brief       → Capture stakeholder requirements (ANALYZE phase)
/bmad-architecture        → Design data architecture (ARCHITECT phase)
/bmad-epics-and-stories   → Decompose into agent tasks (DECOMPOSE phase)
/bmad-parallel-plan       → Find conflict-free parallel waves
/bmad-investigate         → Debug production data issues
/bmad-document-project    → Analyse existing legacy pipelines
```

---

## Before You Move On

- [ ] Can you explain why the parallel-wave rule prevents semantic conflicts?
- [ ] What are the three quality contract severity levels, and what does each trigger?
- [ ] What makes a story "well-scoped" for agent delegation?
- [ ] What's the six-item review checklist for agent-generated pipeline code?
- [ ] What BMAD command would you use to start planning a new data product?

**Coming up in Module 03:** We take the BMAD methodology and apply it to your specific workflows — ETL, DQ, Power BI, schema changes, and the SQL requests that fill your inbox.
