---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# How to Make This Safe Enough to Actually Use

*The patterns that turn experimental into production-grade*

*Module 06 · AI-Native Data Engineering*

---

# The question your stakeholders will ask

> "That sounds interesting. But how do we know it's reliable enough for production?"

That's the right question. And the answer is not "trust the AI."

The answer is: quality gates, audit trails, reviewed PRs, scoped access, tested agents, and graceful fallbacks. The same discipline that makes any system enterprise-grade — applied to AI-native pipelines.

Every pattern in this module exists because a team tried to skip it.

- No quality gate → data trust crisis when bad data hit production
- No audit trail → compliance failure under regulatory review
- No rollback plan → schema change caused a weekend outage
- Schema change ran without rollback plan → outage
- PII flowed through an unscoped MCP server → security incident

**Enterprise AI data engineering is about making speed safe.**

---

# Pattern 1: The Quality Gate

Never promote data without a quality gate.

```
Source Data
    │
    ▼
Transformation Agent
    │
    ▼
Quality Gate Agent ──── FAIL? ──→ Alert + Block + Log
    │
  PASS
    │
    ▼
Target (Warehouse / Report / Consumer)
```

The quality gate is not optional. It is the foundation of data trust.

---

# Pattern 1: Quality Gate — Implementation

```python
def pipeline_gate(quality_report: dict) -> bool:
    """Block promotion on any critical issue."""
    critical = [i for i in quality_report["issues"]
                if i["severity"] == "critical"]
    
    if critical:
        # Log to audit trail
        audit_log.write({
            "event": "pipeline_blocked",
            "reason": [i["description"] for i in critical],
            "timestamp": datetime.utcnow().isoformat(),
            "run_id": quality_report["run_id"]
        })
        raise PipelineBlockedError(f"{len(critical)} critical issues")
    
    return True
```

**Every pipeline, every run. No exceptions.**

---

# Pattern 2: Audit Trail

Every agent action must be logged. Auditors need to answer:
- What data changed?
- When?
- Why? (which pipeline run, which data quality state)
- Who approved the deployment?

```python
AUDIT_SCHEMA = {
    "run_id": str,          # unique per pipeline execution
    "agent": str,           # which agent took this action
    "action": str,          # what was done
    "rows_affected": int,   # data change scope
    "quality_score": int,   # DQ state at time of action
    "approver": str,        # human who merged the PR
    "git_sha": str,         # exact code version used
    "timestamp": str        # UTC ISO 8601
}
```

---

# Pattern 2: Audit Trail — PR Requirement

Every agent-generated change that reaches production must:

```
Agent generates code
    │
    ▼
PR created with:
  - Auto-generated: what changed (diff)
  - Human-written: WHY it changed (PR description)
  - Auto-attached: quality gate report
  - Auto-attached: lineage impact analysis
    │
    ▼
Human review + approval
    │
    ▼
CI/CD: quality gate runs again on staging data
    │
    ▼
Production deployment
```

**The PR is your audit trail. Protect it.**

---

# Pattern 3: Least-Privilege MCP

Every MCP server connection is a potential attack surface.

**Rule**: Grant the minimum access that makes the agent's task possible.

```json
// .mcp.json — scoped connections
{
  "mcpServers": {
    "warehouse-readonly": {
      "description": "Analytics queries only — SELECT, no writes",
      "permissions": ["SELECT"],
      "schemas": ["analytics", "reporting"]
    },
    "warehouse-pipeline": {
      "description": "Pipeline management — INSERT/UPDATE target tables only",
      "permissions": ["INSERT", "UPDATE"],
      "schemas": ["staging", "fact", "agg"],
      "deny": ["DROP", "TRUNCATE", "ALTER"]
    }
  }
}
```

---

# Pattern 3: PII Protection

Any MCP server that can access PII tables requires:

1. **Explicit schema scoping** — PII schema not in analytics MCP
2. **Data masking at the MCP layer** — email → hash, phone → null
3. **Audit log for every PII access** — who asked, what was returned
4. **No PII in agent logs** — never log full records in debug output

```python
# Tool that handles PII safely
{
    "name": "query_customer_data",
    "description": "Returns customer metrics — NOT raw PII. 
                    Email, phone, address are masked automatically.",
    "input_schema": { ... }
}
```

---

# Pattern 4: Idempotent Pipelines

Enterprise pipelines run multiple times: retries, backfills, incident recovery.

**Every pipeline must be safely re-runnable.**

```sql
-- Bad: inserts duplicates on re-run
INSERT INTO fact_revenue SELECT ... FROM staging_revenue;

-- Good: idempotent merge
MERGE INTO fact_revenue AS target
USING staging_revenue AS source
ON target.transaction_id = source.transaction_id
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...;
```

**Require this in every quality contract. The DQ agent should check it.**

---

# Pattern 5: Schema Change Protocol

Schema changes are the most dangerous operation in data engineering.

**Never run a schema change without:**

```
1. Schema evolution agent: classify all changes (breaking vs non-breaking)
2. Pre-deployment checklist generated
3. Forward SQL reviewed by human
4. Rollback SQL documented and tested
5. Downstream impact analysis complete
6. Maintenance window scheduled for breaking changes
7. Communication sent to data consumers
```

**Two-step for NOT NULL additions:**
```sql
-- Step 1: Add nullable
ALTER TABLE orders ADD COLUMN discount_pct DECIMAL(5,2);
-- Step 2: Backfill
UPDATE orders SET discount_pct = 0.0 WHERE discount_pct IS NULL;
-- Step 3: Add constraint (separate deployment after validation)
ALTER TABLE orders ALTER COLUMN discount_pct SET NOT NULL;
```

---

# Pattern 6: Agent Output Classification

Not all agent output is equal. Classify by risk:

| Risk Level | Examples | Required Review |
|---|---|---|
| **Critical** | Schema changes, PII access, prod deployments | Senior engineer + manager |
| **High** | New pipeline to production, QC gate changes | Engineer review + QA gate |
| **Medium** | Transformation logic changes, new aggregations | Peer review + automated test |
| **Low** | Documentation updates, view changes, new columns (nullable) | Automated CI check |

**Match review effort to risk. Don't require heavy process for low-risk changes.**

---

# Pattern 7: The Evals Framework

How do you know your agents are getting better (not worse) over time?

**AgentEvaluator pattern** (from Google ADK):

```python
test_cases = [
    {
        "input": "How many orders did customer C001 place in June?",
        "expected_tools": ["get_schema", "validate_sql", "execute_sql"],
        "expected_output_contains": ["customer_id", "COUNT", "2026-06"],
        "quality_threshold": 0.95
    }
]

# Run after every agent deployment
evaluator.run(agent, test_cases, threshold=0.95)
```

Agents are software. They need regression tests.

---

# Pattern 8: Graceful Degradation

Production pipelines fail. Agents should fail gracefully.

```python
def pipeline_with_fallback(source_data):
    try:
        # Full AI-native pipeline
        result = run_full_agent_pipeline(source_data)
    except AgentTimeoutError:
        # Fall back to last known good state
        result = load_from_cache(max_age_hours=6)
        alert_oncall("Agent timeout — serving cached data")
    except QualityGateBlockedError as e:
        # Data blocked — serve stale rather than bad data
        result = load_previous_run()
        alert_oncall(f"Quality gate blocked: {e}")
    
    return result
```

**Bad data is worse than stale data. Always prefer stale over wrong.**

---

# Enterprise Readiness Checklist

Before calling any AI-native pipeline "production-ready":

```
□ Quality gate implemented (critical blocks, warning alerts)
□ Audit trail: every run logged with run_id, rows, quality score
□ PR required: human review for all agent-generated changes
□ MCP servers scoped to least privilege
□ PII access audited and masked at tool layer
□ All pipelines idempotent (re-runnable safely)
□ Schema change protocol: forward + rollback SQL tested
□ Agent evals suite: regression tests passing
□ Graceful degradation: fallback on agent failure
□ Monitoring: data quality dashboard, not just job status
□ Runbook: on-call knows how to intervene in agent pipeline
```

---

# Module 06 — Key Takeaways

- Quality gates are non-negotiable — block on critical, alert on warning
- Every agent-generated production change needs a PR with human review
- Least-privilege MCP scoping is a security requirement, not a nice-to-have
- All pipelines must be idempotent
- Schema changes need explicit forward and rollback SQL
- Agents need evals — they are software with regressions
- Bad data is worse than stale data — design for graceful degradation

**You have completed the core curriculum. Proceed to hands-on labs in `../data-engineering/`**
