# Module 06: Enterprise Patterns — Reading Guide

## The Shift in Who's Responsible

In a manual data engineering workflow, the engineer is responsible for the quality of what they ship because they wrote it. The judgment is embedded in the code.

In an AI-native workflow, the engineer is responsible for the quality of what they ship because they designed the quality gates and reviewed the output. The judgment is explicit in the contract and the review checklist.

The responsibility doesn't decrease. The location of the judgment changes — from implicit (in the code) to explicit (in the contract and review).

This is actually better for organisations. When judgment is explicit, it can be audited, improved, and transferred. When it's implicit, it leaves when the engineer does.

---

## Pattern 1: The Quality Gate — Design

A quality gate is a blocking check that runs between pipeline stages. It is not optional, not best-effort, and not a dashboard you look at occasionally.

**Anatomy of a quality gate:**

```
After each pipeline stage:
    Run DQ agent checks
    ↓
    Critical failure? → BLOCK promotion + log + alert on-call
    Warning failure?  → LOG + alert team + continue with exclusions
    Info only?        → LOG + continue
```

**The most important design decision:** What counts as critical?

The answer is always: "any failure that would cause a business decision to be made on wrong data." This includes:
- Null primary keys (data is uncountable/unjoinable)
- Duplicate primary keys (aggregations are wrong)
- Revenue sums that deviate from the source by more than your tolerance (Finance can't reconcile)
- Missing required foreign keys (downstream joins will silently drop rows)

The warning vs info boundary is: "would an analyst notice this and escalate?" If yes, it's a warning.

---

## Pattern 2: Audit Trails — What You Actually Need

An audit trail for a data pipeline needs to answer five questions:

1. What data was written, when?
2. Which pipeline version wrote it? (git SHA)
3. What was the data quality state at time of write? (DQ report)
4. Who reviewed and approved the pipeline code? (PR approval)
5. What was the triggering event? (scheduled run, manual trigger, incident response)

**The minimum viable audit record:**
```python
{
    "run_id": "RUN-2026-06-21-08-30-00-abc123",
    "pipeline": "fact_revenue",
    "git_sha": "a1b2c3d4",
    "rows_written": 4823,
    "quality_score": 94,
    "quality_gate_result": "passed_with_warnings",
    "warnings": ["3 null product_ids (guest purchases — expected)"],
    "pr_url": "github.com/org/repo/pull/42",
    "approver": "jane.smith",
    "timestamp": "2026-06-21T08:30:00Z"
}
```

This record goes into a separate `pipeline_runs` table. It is append-only. It is never deleted.

**What auditors actually want:** The ability to trace a specific number in a report back to its source data, including every transformation applied. The audit trail makes this possible. Without it, you're reconstructing history from memory.

---

## Pattern 3: Least-Privilege MCP — The Practical Guide

The principle: grant the minimum access that makes the task possible. No more.

**For analytics workloads (text-to-SQL, exploration):**
```json
{
  "mcpServers": {
    "warehouse-read": {
      "permissions": ["SELECT"],
      "schemas": ["analytics", "reporting", "marts"]
    }
  }
}
```

**For pipeline management (ETL agents):**
```json
{
  "mcpServers": {
    "warehouse-pipeline": {
      "permissions": ["SELECT", "INSERT", "UPDATE"],
      "schemas": ["staging", "fact", "agg"],
      "deny": ["DROP", "TRUNCATE", "ALTER", "CREATE"]
    }
  }
}
```

**PII tables:** Never in the analytics MCP. If an analyst needs de-identified data from a PII table, build a view that masks PII and grant access to the view, not the table.

**Schema migrations:** A separate MCP or a manual process. DDL changes (ALTER, CREATE, DROP) should never be in an automated agent's reach.

---

## Pattern 4: Idempotency — The One Rule That Prevents Most Disasters

An idempotent operation produces the same result when run multiple times with the same input.

Why this matters for data engineering: pipelines re-run. Backfills happen. Incidents occur and recovery means re-running. Every pipeline that is not idempotent will produce duplicates when re-run.

**Making a pipeline idempotent:**

```sql
-- The pattern: MERGE (upsert), not INSERT
MERGE INTO fact_revenue AS target
USING (SELECT * FROM staging_revenue WHERE date = '{{ run_date }}') AS source
ON target.transaction_id = source.transaction_id
WHEN MATCHED THEN UPDATE SET
    amount_usd = source.amount_usd,
    status = source.status,
    updated_at = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN INSERT (
    transaction_id, customer_id, amount_usd, status, created_at, loaded_at
) VALUES (
    source.transaction_id, source.customer_id, source.amount_usd,
    source.status, source.created_at, CURRENT_TIMESTAMP
);
```

**The review checklist item:** For every pipeline an agent generates, ask: "If I run this twice with the same data, do I get duplicate rows?" If yes, it's not idempotent. Send it back.

---

## Pattern 5: Agent Evals — Your Agents Are Software

Agents are not static. They can regress when:
- The model version changes
- The system prompt is updated
- The tools change
- The data schema changes

Without an eval framework, you won't know your agent regressed until it fails in production.

**A minimal eval framework:**

```python
test_cases = [
    {
        "description": "Extract invoice with all fields present",
        "input": CLEAR_INVOICE_TEXT,
        "assertions": [
            lambda r: r["confidence"] >= 0.9,
            lambda r: r["total_amount"] == 8515.03,
            lambda r: len(r["line_items"]) == 3,
        ]
    },
    {
        "description": "Handle missing vendor tax ID gracefully",
        "input": INVOICE_WITHOUT_TAX_ID,
        "assertions": [
            lambda r: r.get("vendor", {}).get("tax_id") is None,
            lambda r: r["confidence"] >= 0.7,
        ]
    }
]

# Run after every deployment or model version change
for case in test_cases:
    result = run_agent(case["input"])
    failures = [a for a in case["assertions"] if not a(result)]
    assert not failures, f"{case['description']}: {failures}"
```

Run this in CI. Block deployments if eval score drops below threshold. This is not overhead — it's the same discipline you'd apply to any other production system.

---

## Pattern 6: Graceful Degradation — Because Things Will Break

Design every AI-native pipeline with an answer to: "What happens when the agent fails?"

Options in order of preference:
1. **Retry with backoff** — for transient failures (rate limits, timeouts)
2. **Serve last known good data** — for quality gate failures (stale beats wrong)
3. **Fall back to previous pipeline version** — for agent regression failures
4. **Alert and halt** — for catastrophic failures (data integrity at risk)

**Never:** silently continue with bad data. Bad data that reaches stakeholders destroys data trust in ways that take months to rebuild.

The rule: **stale data is better than wrong data**. When in doubt, halt and alert.

---

## Production Readiness Checklist

This checklist gates any AI-native pipeline from going to production:

```
Infrastructure:
□ Quality gate implemented with correct severity thresholds
□ Audit log table exists and pipeline writes to it
□ MCP permissions scoped to minimum required
□ PII tables excluded from analytics MCP

Code Quality:
□ All pipelines are idempotent (re-run safe)
□ Rollback SQL exists and has been tested for all schema changes
□ Agent eval suite passes at ≥95% threshold
□ PR review completed with six-item checklist signed off

Operations:
□ On-call runbook documents how to intervene in agent pipeline
□ Quality gate alerts route to correct channel/person
□ Graceful degradation tested (what happens when agent times out?)
□ Data quality dashboard shows data health, not just job status
```

If any item is unchecked, the pipeline does not go to production. No exceptions.

---

## Before You Move On

- [ ] What are your critical quality gates for your primary pipeline?
- [ ] What five fields would you include in your pipeline audit record?
- [ ] What's the smallest MCP permission set for your analytics use case?
- [ ] Can you state whether all your current pipelines are idempotent?
- [ ] What would a basic eval suite look like for one of your existing pipelines?
