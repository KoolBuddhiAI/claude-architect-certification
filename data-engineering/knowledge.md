# Agents for Data Engineering — Knowledge Base

## Why Agents for Data Engineering?

Data engineering is a natural fit for agentic patterns: pipelines fail unpredictably, data has quality issues that require investigation, schemas drift, and SQL needs iterative refinement. Agents excel where the path to completion is non-linear and requires tool-driven decision-making.

---

## Ecosystem Landscape (2026)

### Google ADK Approach
Google's Agent Development Kit (ADK) data engineering sample (github.com/google/adk-samples) focuses on:
- **Dataform pipeline ownership** — agents own SQLx files, UDFs, stored procedures end-to-end
- **BigQuery + Vertex AI** as the execution backend
- **`AgentEvaluator`** — test-first validation of agent responses against expected outputs
- **Environment-driven config** via `.env` — project, model, workspace all injectable
- Key thesis: agents own Dataform workspaces entirely, not just generate SQL snippets

### Microsoft Fabric + Claude
Microsoft released `skills-for-fabric` (github.com/microsoft/skills-for-fabric) — official Claude Code skill bundles:

| Skill Bundle | What It Enables |
|---|---|
| `fabric-authoring` | Create pipelines, notebooks, semantic models via Fabric REST API |
| `fabric-consumption` | Query Warehouses, Lakehouses, Power BI semantic models |
| `fabric-operations` | Diagnose slow queries, warehouse performance |
| `powerbi-authoring` | Semantic model creation, PBIR reports, publish, iterate |

**Migration path**: Power BI Q&A (legacy NL feature) retiring Dec 2026 → replacement is Claude + Fabric MCP. Claude queries semantic models, writes DAX, authors reports, troubleshoots pipelines from Claude Code.

### BMAD Method for Data Engineers
"Breakthrough Method for Agile AI-Driven Development" (github.com/bmad-code-org/BMAD-METHOD):
- 20 slash commands: `/bmad-architecture`, `/bmad-parallel-plan`, `/bmad-epics-and-stories`
- Core insight for data: **plan data lineage and dependencies BEFORE parallel pipeline development** — prevents semantic conflicts when multiple agents work on the same warehouse
- Works with Claude Code via skills install

### Superpowers Framework
Community framework (40.9k GitHub stars, in Anthropic marketplace):
- Full multi-agent lifecycle: brainstorm → plan → subagent execution → TDD → review → merge
- Data pattern: pin one MCP per external system (Postgres, Fabric, Snowflake) + thin skills for orchestration

### The 2026 Pattern
```
MCP servers  = connectivity  (GitHub, Postgres, Fabric, Snowflake, BigQuery)
Skills       = methodology   (BMAD, Superpowers, domain knowledge)
Agents       = execution     (ETL, quality checks, SQL generation, schema evolution)
```

---

## Core Patterns

### 1. Stage-as-Tool (ETL)
Map each ETL stage to a tool: `fetch_page`, `transform_record`, `load_records`. The agent orchestrates the sequence, handles partial failures, and decides when to retry vs skip vs abort — no hardcoded control flow in the host application.

**Key insight**: Return errors as data (not exceptions) from tools. `{"error": "null amount", "record_id": "X"}` keeps the agent loop alive and lets the agent decide how to handle it.

### 2. Schema-as-Tool-Input (Text-to-SQL)
Pass schema definitions as tool inputs rather than embedding them in system prompts:
- Dynamic introspection at query time — no stale column names
- Accurate column-level context for SQL generation
- Token usage scales with query complexity, not total schema size

### 3. Validation-Retry Loop (SQL & Transformations)
Never run LLM-generated SQL without validation:
```
generate SQL → validate syntax → dry-run EXPLAIN → execute → if error, retry with correction
```
Max 3 retries. Return last attempt with error rather than crashing.

### 4. Structured Quality Reports
Use schema-enforced tool output for DQ reports:
- Consistent severity taxonomy: `critical / warning / info`
- Machine-readable output for dashboards and alerting
- Downstream automation: block pipeline on critical issues

### 5. Explicit Context in Subagents
In multi-agent pipelines, each subagent receives a complete snapshot of upstream results. Never rely on shared state. Pass table names, row counts, schema versions, and all relevant metadata explicitly.

### 6. Pipeline Gate Pattern (Multi-Agent)
Quality agent reports facts; orchestrator makes decisions:
- `critical` issues → abort, escalate
- `warning` issues → proceed with flagged records excluded
- `info` issues → proceed, log only

---

## Tool Design Principles for Data Engineering

| Principle | Why It Matters |
|-----------|----------------|
| Include data shape in descriptions | Agent picks the right tool without hallucinating column names |
| Return counts not just success/fail | Agent makes informed retry/skip decisions |
| Separate transform from load | Allows partial recovery — reload without re-transforming |
| Always include a stats/summary tool | Agent verifies its own work before reporting completion |
| Dry-run before destructive operations | EXPLAIN before execute; schema diff before migration |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Raising exceptions from data tools | Kills the agent loop on a single bad record | Return `{"error": "..."}` as data |
| Embedding full schema in system prompt | Stale on schema changes; wastes tokens | Use `get_schema` tool at runtime |
| One-shot SQL generation (no retry) | ~30% of generated SQL has syntax errors | Validate + retry loop, max 3 attempts |
| Vague tool descriptions | Agent confuses `orders` vs `order_items` | Include table purpose and key columns in description |
| Mixing transform and load logic | Can't recover partial loads | Separate `transform_record` and `load_records` tools |
| Planning after implementation | Semantic conflicts in multi-agent pipelines | BMAD: plan lineage and dependencies first |

---

## CCA-F Domain Alignment

| Data Engineering Pattern | Primary Domain | Secondary Domain |
|---|---|---|
| ETL pipeline agent | Agentic Architecture (27%) | Tool Design (18%) |
| Data quality agent | Prompt Engineering (20%) | Tool Design (18%) |
| Text-to-SQL agent | Tool Design (18%) | Context Management (15%) |
| Schema evolution agent | Agentic Architecture (27%) | Prompt Engineering (20%) |
| Multi-agent pipeline | Agentic Architecture (27%) | Context Management (15%) |

---

## Scenarios in This Folder

| # | Scenario | Key Pattern | Stack Parallel |
|---|---|---|---|
| 01 | ETL Pipeline Agent | Stage-as-tool, error-as-data, dedup | Fabric Data Pipeline / Dataform |
| 02 | Data Quality Agent | Systematic checks, schema-enforced report | Fabric DQ rules / dbt tests |
| 03 | Text-to-SQL Agent | Runtime schema introspection, validation-retry | Fabric semantic model / BigQuery |
| 04 | Schema Evolution Agent | Breaking/non-breaking detection, migration SQL | Fabric warehouse / Alembic |
| 05 | Multi-Agent Pipeline | Orchestrator coordinates ingestion→QA→transform | Fabric Lakehouse medallion pattern |
