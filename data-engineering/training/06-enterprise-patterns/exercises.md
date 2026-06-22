# Module 06: Hands-On Exercises

## Exercise 1 — Quick (20 min): Define Your Quality Gates

**Goal:** Translate the quality gate pattern into concrete thresholds for a real pipeline.

Choose one of your existing pipelines (or the one from Module 03's BMAD exercise).

Define the quality contract:

```markdown
## Quality Contract: [Pipeline / Table Name]

### Critical Gates (block promotion if violated)
1. [Column]: [Condition] — Why: [business impact if this fails]
2. [Column]: [Condition] — Why:
3. [Sum / Count check]: [Tolerance] — Why:

### Warning Gates (alert, continue with exclusions)
1. [Column]: [Condition] — How to handle: [exclude records / flag / accept]
2. [Column]: [Condition] — How to handle:

### Info (log only)
1. [Condition] — Note:

### SLA
Must complete by: [time] UTC
Alert if not started by: [time] UTC
```

Then ask yourself: if the last data quality issue your team dealt with had been caught by these gates, would it have been blocked?

If no: what gate is missing?

---

## Exercise 2 — Medium (45 min): Run the Full Data Engineering Stack

**Goal:** Run all five data-engineering scenarios and observe the quality gate, audit, and agent patterns in action.

```bash
cd data-engineering
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
```

Run each scenario and answer these questions:

**Scenario 01 (ETL Pipeline Agent):**
- What happens to the record with `null` amount? (Trace the error-as-data pattern)
- What happens to the duplicate record? (Trace the dedup logic)
- Would this pipeline produce duplicates if run twice? (Idempotency check)

**Scenario 02 (Data Quality Agent):**
- How many issues does it find?
- Which would you classify differently?
- What critical gate would you add?

**Scenario 03 (Text-to-SQL Agent):**
- Does the validation-retry loop trigger on any of the three queries?
- What happens if you ask it about a column that doesn't exist?

**Scenario 04 (Schema Evolution Agent):**
- Which changes does it correctly classify as breaking?
- Does the rollback SQL cover the most dangerous change?

**Scenario 05 (Multi-Agent Pipeline):**
- At what quality risk level does the orchestrator choose to proceed vs. abort?
- How would you change that threshold for a Finance pipeline vs. a marketing analytics pipeline?

**Deliverable:** 5 paragraphs (one per scenario) with your observations and one thing you'd change in each.

---

## Exercise 3 — Deep (90 min): Build the Enterprise Safety Layer for Your Pipeline

**Goal:** Take the pipeline from Module 03's BMAD exercise and add the full enterprise safety layer.

**Part 1 — Quality gate implementation (30 min)**

Using `data-engineering/02-data-quality-agent/main.py` as a reference, implement the quality gates you defined in Exercise 1 as actual tool calls in a Python quality agent.

Your agent should:
- Run at least 4 checks (nulls, duplicates, at least one range check, at least one enum check)
- Output a structured report with severity classification
- Return a boolean `should_promote` based on whether any critical gates failed

**Part 2 — Audit trail (20 min)**

Add an audit logging function that writes to a SQLite table after each pipeline run:

```python
def log_pipeline_run(
    run_id: str,
    pipeline_name: str,
    rows_written: int,
    quality_report: dict,
    promoted: bool
) -> None:
    # Write to pipeline_runs table
    # Include: run_id, pipeline, rows, quality_score, gate_result, timestamp
```

Verify you can query the audit log and see: run_id, quality score, whether it was promoted, and when.

**Part 3 — Idempotency test (10 min)**

For the pipeline from Module 03's BMAD exercise:
- Run the ETL agent from Scenario 01 twice with the same input data
- Check the row count after each run — are there duplicates?
- If yes: identify exactly where the non-idempotent operation is and describe the fix

**Part 4 — Eval suite (30 min)**

Write three test cases for one of your agents:

```python
test_cases = [
    {
        "description": "Happy path — all fields present",
        "input": "...",
        "assertions": [
            lambda r: ...,  # check specific output values
        ]
    },
    {
        "description": "Edge case — [specific edge case]",
        "input": "...",
        "assertions": [...]
    },
    {
        "description": "Graceful degradation — bad input",
        "input": "...",
        "assertions": [
            lambda r: r is not None,  # at minimum, doesn't crash
            lambda r: r.get("confidence", 1.0) < 0.5  # low confidence flagged
        ]
    }
]
```

Run them. All three should pass. If any fail, fix the agent or the test case and understand why it failed.

**Deliverable:** Three files:
1. `quality_gate.py` — quality agent with your gates
2. `audit_log.py` — audit logging function + schema
3. `evals.py` — three test cases, all passing

These three files are the foundation of an enterprise-ready agent pipeline.
