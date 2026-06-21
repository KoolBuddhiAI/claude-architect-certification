# Scenario DE-02: Data Quality Agent

## What This Demonstrates
An agent that systematically runs a battery of quality checks on a dataset and produces a structured, schema-enforced quality report — usable as a pipeline gate or monitoring alert.

## CCA-F Domain Alignment
| Domain | Weight | Coverage |
|--------|--------|----------|
| Prompt Engineering & Structured Output | 20% | Schema-enforced report via tool, severity taxonomy |
| Tool Design & MCP Integration | 18% | Check-per-tool design, enum validation |
| Agentic Architecture | 27% | Systematic multi-tool execution, completeness verification |

## Key Architectural Decisions

### One Tool per Check Type
Separate tools for: `check_nulls`, `check_duplicates`, `check_value_ranges`, `check_enum_values`, `check_date_format`. Each returns structured data the agent can reason about before compiling the report.

### Schema-Enforced Report via Tool
`submit_quality_report` takes a full JSON Schema with severity enums (`critical/warning/info`), score, and per-issue recommendations. Guarantees machine-readable output for downstream automation.

### Systematic Execution
System prompt instructs: "run every check before submitting." Agent cannot short-circuit to the report tool after just one check — it must exhaust the full battery.

### Severity Taxonomy
| Severity | Trigger | Pipeline Action |
|----------|---------|-----------------|
| critical | Nulls on PK, data corruption | Block pipeline |
| warning | Outliers, enum violations | Alert, continue |
| info | Style/formatting issues | Log only |

## Issues Seeded in Sample Data
- Negative `amount` value (ORD-002)
- Null `customer_id` (ORD-003)
- Invalid `status` enum value (ORD-004)
- Statistical outlier amount (ORD-005)
- Malformed date (ORD-006)
- Duplicate primary key (ORD-001)
- Unknown region value (ORD-009)

## Anti-Patterns Avoided
| Anti-Pattern | Correct Approach |
|---|---|
| Free-text quality summary | Schema-enforced `submit_quality_report` tool |
| Single catch-all "check_all" tool | One tool per check type for composability |
| Boolean pass/fail only | Score + per-issue severity + recommendation |

## Learning Objectives
1. Design a check-per-tool battery for systematic data validation
2. Use schema-enforced tools for machine-readable quality reports
3. Build severity taxonomy that drives downstream pipeline decisions
4. Implement complete-before-submit pattern via system prompt

## How to Run
```bash
pip install -r ../requirements.txt
export ANTHROPIC_API_KEY=your_key
python main.py
```
