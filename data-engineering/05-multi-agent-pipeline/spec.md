# Scenario DE-05: Multi-Agent Data Pipeline

## What This Demonstrates
An orchestrator agent that coordinates three specialized subagents (ingestion, quality, transformation) into a complete data pipeline — demonstrating the orchestrator-subagent pattern in a data engineering context.

## CCA-F Domain Alignment
| Domain | Weight | Coverage |
|--------|--------|----------|
| Agentic Architecture & Orchestration | 27% | Orchestrator-subagent, task decomposition, explicit context |
| Context Management & Reliability | 15% | Context budgeting, stage gate decisions |
| Tool Design & MCP Integration | 18% | Subagent delegation tools with typed inputs |

## Architecture

```
Orchestrator
├── run_ingestion_agent(source, config)
│   └── Fetches raw data, returns {records, metadata}
├── run_quality_agent(records, rules)
│   └── Validates data, returns {passed, failed, report}
└── run_transformation_agent(records, target_schema)
    └── Transforms and loads, returns {loaded, skipped, errors}
```

## Key Architectural Decisions

### Pipeline Gate Pattern
Orchestrator uses quality check results to make go/no-go decisions before transformation:
- `critical` issues → abort pipeline, escalate
- `warning` issues → proceed with flagged records excluded
- `info` issues → proceed normally

This logic lives in the **orchestrator**, not in individual subagents. Subagents report facts; orchestrator makes decisions.

### Explicit Context Passing
Each subagent receives a complete task brief including:
- Source metadata (row counts, column names, data types)
- Upstream results (quality report details for transformation agent)
- Target schema and load configuration

No subagent assumes knowledge from prior steps — all context is in the delegation tool call.

### Subagent Specialization
| Subagent | Responsibility | Model Choice |
|---|---|---|
| Ingestion | Fetch, paginate, basic normalize | Sonnet (fast, cost-efficient) |
| Quality | Statistical analysis, classification | Sonnet (reasoning-heavy) |
| Transformation | Schema mapping, type coercion | Haiku (structured, repetitive) |

### Observability
Orchestrator collects a pipeline run log: each stage's timing, row counts, and status. Final report includes full lineage: source → ingested → passed quality → loaded.

## Pipeline Run Report Schema
```json
{
  "run_id": "RUN-2026-001",
  "status": "completed|failed|partial",
  "stages": [
    {"stage": "ingestion", "rows_fetched": 100, "duration_ms": 1200},
    {"stage": "quality",   "passed": 94, "failed": 6, "risk": "warning"},
    {"stage": "transform", "loaded": 94, "skipped": 0, "errors": 0}
  ],
  "final_row_count": 94
}
```

## Anti-Patterns Avoided
| Anti-Pattern | Correct Approach |
|---|---|
| Subagents share state via global dict | All context passed explicitly in delegation calls |
| Orchestrator makes no decisions | Orchestrator owns the gate logic, not subagents |
| All stages use same model | Match model to task: reasoning vs structured vs fast |
| No pipeline observability | Structured run log with per-stage metrics |

## Learning Objectives
1. Apply orchestrator-subagent pattern to a multi-stage data pipeline
2. Implement pipeline gate decisions in the orchestrator layer
3. Pass explicit context including upstream results to downstream subagents
4. Match model selection to subagent workload characteristics
5. Build structured pipeline observability from stage results

## How to Run
```bash
pip install -r ../requirements.txt
export ANTHROPIC_API_KEY=your_key
python main.py
```
