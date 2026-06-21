# Scenario DE-01: ETL Pipeline Agent

## What This Demonstrates
An agent that executes a full extract-transform-load pipeline across paginated API data, handling partial failures, deduplication, and type normalization — without hardcoded control flow in the caller.

## CCA-F Domain Alignment
| Domain | Weight | Coverage |
|--------|--------|----------|
| Agentic Architecture & Orchestration | 27% | Agent loop, stage sequencing, failure handling |
| Tool Design & MCP Integration | 18% | Stage-as-tool pattern, error-as-data |
| Prompt Engineering | 20% | System prompt driving correct pipeline order |

## Key Architectural Decisions

### Stage-as-Tool Pattern
Each ETL stage is a separate tool: `fetch_page`, `transform_record`, `load_records`, `get_load_stats`. The agent sequences them — no hardcoded `for page in pages` in the host code.

### Error-as-Data (not Exceptions)
`transform_record` returns `{"error": "...", "record_id": "X"}` for bad records rather than raising exceptions. This keeps the agent loop alive. `load_records` skips error objects and counts them as `failed`.

### Deduplication at Load Time
`load_records` checks a seen-IDs set before inserting. Duplicate records are counted as `skipped_duplicates` — distinguishable from failures. Agent gets accurate counts for the final report.

### Batched Loading
Agent fetches page → transforms all records → loads batch. One `load_records` call per page, not per record. Reduces round-trips and matches real warehouse bulk-insert patterns.

## Data Flow
```
fetch_page(0) → [raw records]
  → transform_record(each) → [transformed | error]
  → load_records(batch) → {inserted, skipped, failed}
fetch_page(1) → repeat
get_load_stats() → final report
```

## Anti-Patterns Avoided
| Anti-Pattern | Correct Approach |
|---|---|
| `raise ValueError` on bad record | Return `{"error": "..."}` — agent decides to skip |
| Loop in caller code | Agent sequences pages via tool calls |
| Load one record at a time | Batch per page for efficiency |
| No dedup tracking | `skipped_duplicates` count separate from `failed` |

## Learning Objectives
1. Implement stage-as-tool ETL pattern
2. Design error-as-data for resilient pipelines
3. Handle pagination through agent tool calls
4. Separate deduplication concerns from transformation

## How to Run
```bash
pip install -r ../requirements.txt
export ANTHROPIC_API_KEY=your_key
python main.py
```
