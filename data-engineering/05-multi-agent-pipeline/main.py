"""
Multi-Agent Data Pipeline — Scenario DE-05
Demonstrates: orchestrator-subagent pattern, pipeline gate decisions, explicit context passing.
Coordinates: ingestion → quality gate → transformation subagents.
"""
import anthropic
import json
import sqlite3
import uuid
from datetime import datetime, timezone

client = anthropic.Anthropic()
MODEL_ORCHESTRATOR = "claude-sonnet-4-6"
MODEL_SUBAGENT = "claude-haiku-4-5-20251001"  # faster/cheaper for structured subtasks

# ── Simulated source data ────────────────────────────────────────────────────
RAW_SOURCE = [
    {"event_id": "E001", "ts": "2026-06-21T08:00:00Z", "user_id": "U1", "action": "purchase", "amount": 299.0,  "product": "Laptop Stand"},
    {"event_id": "E002", "ts": "2026-06-21T08:05:00Z", "user_id": None, "action": "view",     "amount": None,    "product": "Keyboard"},      # null user
    {"event_id": "E003", "ts": "2026-06-21T08:10:00Z", "user_id": "U2", "action": "purchase", "amount": -99.0,  "product": "Mouse"},           # negative amount
    {"event_id": "E004", "ts": "2026-06-21T08:15:00Z", "user_id": "U3", "action": "purchase", "amount": 149.0,  "product": "Webcam"},
    {"event_id": "E005", "ts": "2026-06-21T08:20:00Z", "user_id": "U1", "action": "refund",   "amount": 299.0,  "product": "Laptop Stand"},
    {"event_id": "E006", "ts": "2026-06-21T08:25:00Z", "user_id": "U4", "action": "purchase", "amount": 79.0,   "product": "USB Hub"},
    {"event_id": "E001", "ts": "2026-06-21T08:00:00Z", "user_id": "U1", "action": "purchase", "amount": 299.0,  "product": "Laptop Stand"},    # duplicate
]

# ── Target warehouse ─────────────────────────────────────────────────────────
conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE events (
        event_id   TEXT PRIMARY KEY,
        ts         TEXT NOT NULL,
        user_id    TEXT NOT NULL,
        action     TEXT NOT NULL,
        amount_usd REAL,
        product    TEXT NOT NULL,
        loaded_at  TEXT NOT NULL
    )
""")
conn.commit()

# ── Subagent runners ─────────────────────────────────────────────────────────
def run_ingestion_subagent(source_description: str) -> dict:
    """Fetch and normalize raw source data."""
    response = client.messages.create(
        model=MODEL_SUBAGENT,
        max_tokens=1024,
        system=(
            "You are a data ingestion specialist. Analyze the provided raw data and return a structured "
            "JSON summary with: total_records, column_names, sample_issues (nulls/duplicates spotted), "
            "and data_ready=true. Keep your response as a single JSON object."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"{source_description}\n\n"
                f"Raw data ({len(RAW_SOURCE)} records):\n{json.dumps(RAW_SOURCE[:3], indent=2)}\n"
                f"... and {len(RAW_SOURCE)-3} more records.\n"
                f"Column names: {list(RAW_SOURCE[0].keys())}\n"
                f"Total records: {len(RAW_SOURCE)}\n"
                "Return a JSON summary."
            ),
        }],
    )
    try:
        text = response.content[0].text
        start = text.find("{")
        return json.loads(text[start:text.rfind("}")+1]) if start != -1 else {
            "total_records": len(RAW_SOURCE), "column_names": list(RAW_SOURCE[0].keys()),
            "sample_issues": ["nulls in user_id", "negative amounts", "duplicate event_ids"],
            "data_ready": True,
        }
    except Exception:
        return {"total_records": len(RAW_SOURCE), "column_names": list(RAW_SOURCE[0].keys()), "data_ready": True}


def run_quality_subagent(records_info: str, rules: str) -> dict:
    """Run quality checks and return pass/fail/report."""
    # Compute checks directly (subagent does the classification reasoning)
    nulls = [r["event_id"] for r in RAW_SOURCE if r.get("user_id") is None]
    dupes = {}
    seen = {}
    for r in RAW_SOURCE:
        if r["event_id"] in seen:
            dupes[r["event_id"]] = True
        seen[r["event_id"]] = True
    negatives = [r["event_id"] for r in RAW_SOURCE if r.get("amount") is not None and r["amount"] < 0]

    issues = []
    if nulls:
        issues.append({"check": "nulls", "severity": "warning", "affected": nulls, "count": len(nulls)})
    if dupes:
        issues.append({"check": "duplicates", "severity": "warning", "affected": list(dupes.keys()), "count": len(dupes)})
    if negatives:
        issues.append({"check": "negative_amounts", "severity": "warning", "affected": negatives, "count": len(negatives)})

    critical = [i for i in issues if i["severity"] == "critical"]
    warning = [i for i in issues if i["severity"] == "warning"]
    valid_records = [r for r in RAW_SOURCE
                     if r.get("user_id") is not None
                     and r.get("amount", 0) >= 0
                     and r["event_id"] not in dupes]

    return {
        "total_checked": len(RAW_SOURCE),
        "passed": len(valid_records),
        "failed": len(RAW_SOURCE) - len(valid_records),
        "issues": issues,
        "risk_level": "high" if critical else ("warning" if warning else "low"),
        "valid_records": valid_records,
    }


def run_transform_subagent(valid_records: list, target_schema: str) -> dict:
    """Transform and load valid records into the warehouse."""
    loaded = skipped = errors = 0
    loaded_ids = set()

    for rec in valid_records:
        if rec["event_id"] in loaded_ids:
            skipped += 1
            continue
        try:
            conn.execute(
                "INSERT INTO events VALUES (?,?,?,?,?,?,?)",
                (rec["event_id"], rec["ts"], rec["user_id"], rec["action"],
                 rec.get("amount"), rec["product"], datetime.now(timezone.utc).isoformat()),
            )
            conn.commit()
            loaded_ids.add(rec["event_id"])
            loaded += 1
        except Exception:
            errors += 1

    total_rows = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    return {"loaded": loaded, "skipped_duplicates": skipped, "errors": errors, "total_in_warehouse": total_rows}


# ── Orchestrator tools ────────────────────────────────────────────────────────
orchestrator_tools = [
    {
        "name": "run_ingestion",
        "description": (
            "Delegate data ingestion to the ingestion subagent. "
            "Returns: total_records, column_names, sample_issues, data_ready. "
            "Run this first. Include full context in source_description — subagent has no prior memory."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"source_description": {"type": "string", "description": "Full description of the data source, expected schema, and any known issues"}},
            "required": ["source_description"],
        },
    },
    {
        "name": "run_quality_check",
        "description": (
            "Delegate quality validation to the quality subagent. "
            "Returns: passed, failed, issues (with severity), risk_level, valid_records. "
            "Run after ingestion. Pass the full ingestion result as context."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "records_info": {"type": "string", "description": "Ingestion result summary and schema info"},
                "rules": {"type": "string", "description": "Quality rules to enforce (nulls, ranges, enums, duplicates)"},
            },
            "required": ["records_info", "rules"],
        },
    },
    {
        "name": "run_transformation",
        "description": (
            "Delegate transformation and loading to the transform subagent. "
            "ONLY call if quality risk_level is 'low' or 'warning' (not 'high'). "
            "Pass only valid_records from the quality result — do not pass failed records."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "valid_record_count": {"type": "integer", "description": "Number of records to transform"},
                "target_schema": {"type": "string", "description": "Target table schema definition"},
            },
            "required": ["valid_record_count", "target_schema"],
        },
    },
    {
        "name": "submit_pipeline_report",
        "description": "Submit the final pipeline run report after all stages complete (or after aborting on critical issues).",
        "input_schema": {
            "type": "object",
            "properties": {
                "run_id": {"type": "string"},
                "status": {"type": "string", "enum": ["completed", "completed_with_warnings", "failed", "aborted"]},
                "stages": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "stage": {"type": "string"},
                            "status": {"type": "string"},
                            "rows_in": {"type": "integer"},
                            "rows_out": {"type": "integer"},
                            "notes": {"type": "string"},
                        },
                        "required": ["stage", "status"],
                    },
                },
                "final_row_count": {"type": "integer"},
                "issues_summary": {"type": "string"},
            },
            "required": ["run_id", "status", "stages", "final_row_count"],
        },
    },
]


# ── Orchestrator dispatch ────────────────────────────────────────────────────
_quality_result: dict = {}  # shared between orchestrator and transform


def orchestrator_dispatch(name: str, inp: dict) -> dict:
    global _quality_result
    if name == "run_ingestion":
        return run_ingestion_subagent(inp["source_description"])
    if name == "run_quality_check":
        _quality_result = run_quality_subagent(inp["records_info"], inp["rules"])
        return _quality_result
    if name == "run_transformation":
        valid = _quality_result.get("valid_records", [])
        return run_transform_subagent(valid, inp["target_schema"])
    if name == "submit_pipeline_report":
        return inp
    return {"error": f"Unknown tool: {name}"}


# ── Orchestrator agent loop ───────────────────────────────────────────────────
def run_pipeline_orchestrator() -> dict:
    run_id = f"RUN-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print(f"Pipeline run: {run_id}\n")

    messages = [{
        "role": "user",
        "content": (
            f"Execute the full data pipeline (run_id: {run_id}).\n\n"
            "Source: user events stream with fields: event_id, ts, user_id, action, amount, product.\n"
            "Quality rules: no null user_id (warning), no negative amounts (warning), no duplicate event_ids (warning).\n"
            "Target schema: events(event_id PK, ts, user_id NOT NULL, action, amount_usd, product, loaded_at).\n\n"
            "Pipeline: run_ingestion → run_quality_check → gate decision → run_transformation (if not high risk) → submit_pipeline_report.\n"
            "Gate: proceed if risk_level is 'low' or 'warning'; abort if 'high'. Exclude failed records from transformation."
        ),
    }]
    system = (
        "You are a data pipeline orchestrator. Coordinate specialized subagents in sequence.\n"
        "CRITICAL: Subagents have NO shared memory — pass all relevant context explicitly in every call.\n"
        "Gate rule: NEVER call run_transformation if quality risk_level='high'. Abort and report instead.\n"
        "For 'warning' risk: proceed but note excluded records in the pipeline report."
    )

    while True:
        response = client.messages.create(
            model=MODEL_ORCHESTRATOR, max_tokens=2048, system=system,
            tools=orchestrator_tools, messages=messages,
        )
        if response.stop_reason == "end_turn":
            return {"narrative": next((b.text for b in response.content if hasattr(b, "text")), "")}
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  [→ {block.name}]")
                    result = orchestrator_dispatch(block.name, block.input)
                    if block.name == "submit_pipeline_report":
                        return result
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)})
            messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    report = run_pipeline_orchestrator()
    print(f"\n{'='*60}\nPIPELINE REPORT\n{'='*60}")
    print(json.dumps(report, indent=2))
