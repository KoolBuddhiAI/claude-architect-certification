"""
Data Quality Agent — Scenario DE-02
Demonstrates: check-per-tool battery, schema-enforced quality report, severity taxonomy.
"""
import anthropic
import json
import re
from collections import Counter
from statistics import mean, stdev

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

# ── Sample dataset with seeded quality issues ────────────────────────────────
DATASET = [
    {"order_id": "ORD-001", "customer_id": "C001", "amount": 150.0,    "status": "completed", "date": "2026-06-01", "region": "US"},
    {"order_id": "ORD-002", "customer_id": "C002", "amount": -50.0,    "status": "completed", "date": "2026-06-02", "region": "EU"},      # negative amount
    {"order_id": "ORD-003", "customer_id": None,   "amount": 200.0,    "status": "pending",   "date": "2026-06-03", "region": "US"},      # null customer_id
    {"order_id": "ORD-004", "customer_id": "C003", "amount": 75.5,     "status": "bad_status","date": "2026-06-03", "region": "APAC"},    # invalid enum
    {"order_id": "ORD-005", "customer_id": "C004", "amount": 9999999., "status": "completed", "date": "2026-06-04", "region": "US"},      # outlier
    {"order_id": "ORD-006", "customer_id": "C005", "amount": 300.0,    "status": "completed", "date": "not-a-date", "region": "EU"},      # bad date
    {"order_id": "ORD-007", "customer_id": "C006", "amount": 120.0,    "status": "completed", "date": "2026-06-05", "region": "US"},
    {"order_id": "ORD-001", "customer_id": "C001", "amount": 150.0,    "status": "completed", "date": "2026-06-01", "region": "US"},      # duplicate
    {"order_id": "ORD-008", "customer_id": "C007", "amount": 85.0,     "status": "refunded",  "date": "2026-06-06", "region": "US"},
    {"order_id": "ORD-009", "customer_id": "C008", "amount": 440.0,    "status": "completed", "date": "2026-06-07", "region": "UNKNOWN"}, # unknown region
]

# ── Tool definitions ─────────────────────────────────────────────────────────
tools = [
    {
        "name": "check_nulls",
        "description": "Check every column for null/missing values. Returns per-column null count and percentage.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "check_duplicates",
        "description": "Detect duplicate rows by order_id primary key. Returns duplicate IDs and total duplicate row count.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "check_value_ranges",
        "description": (
            "Validate a numeric column for anomalous values. "
            "Detects negatives and statistical outliers (>3 std deviations from mean). "
            "Column must exist in the dataset."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"column": {"type": "string", "description": "Numeric column name, e.g. 'amount'"}},
            "required": ["column"],
        },
    },
    {
        "name": "check_enum_values",
        "description": (
            "Validate a column against an allowed value set. "
            "Returns invalid values and the order_ids of affected rows."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "column": {"type": "string"},
                "allowed_values": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["column", "allowed_values"],
        },
    },
    {
        "name": "check_date_format",
        "description": "Validate a date column for YYYY-MM-DD format. Returns malformed values and their order_ids.",
        "input_schema": {
            "type": "object",
            "properties": {"column": {"type": "string", "description": "Date column name"}},
            "required": ["column"],
        },
    },
    {
        "name": "submit_quality_report",
        "description": "Submit the final structured quality report. Call ONLY after running all checks.",
        "input_schema": {
            "type": "object",
            "properties": {
                "overall_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "total_records": {"type": "integer"},
                "issues": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "check": {"type": "string"},
                            "severity": {"type": "string", "enum": ["critical", "warning", "info"]},
                            "affected_records": {"type": "integer"},
                            "description": {"type": "string"},
                            "recommendation": {"type": "string"},
                        },
                        "required": ["check", "severity", "affected_records", "description", "recommendation"],
                    },
                },
                "summary": {"type": "string"},
            },
            "required": ["overall_score", "total_records", "issues", "summary"],
        },
    },
]


# ── Tool implementations ──────────────────────────────────────────────────────
def check_nulls() -> dict:
    cols = DATASET[0].keys()
    return {
        col: {"null_count": sum(1 for r in DATASET if r.get(col) is None),
              "null_pct": round(sum(1 for r in DATASET if r.get(col) is None) / len(DATASET) * 100, 1)}
        for col in cols
    }


def check_duplicates() -> dict:
    ids = [r["order_id"] for r in DATASET]
    dupes = {k: v for k, v in Counter(ids).items() if v > 1}
    return {"duplicate_ids": dupes, "total_extra_rows": sum(v - 1 for v in dupes.values())}


def check_value_ranges(column: str) -> dict:
    vals = [r[column] for r in DATASET if isinstance(r.get(column), (int, float))]
    if not vals:
        return {"error": f"No numeric values found in '{column}'"}
    avg, sd = mean(vals), (stdev(vals) if len(vals) > 1 else 0)
    return {
        "min": min(vals), "max": max(vals), "mean": round(avg, 2),
        "negatives": [r["order_id"] for r in DATASET if isinstance(r.get(column), (int, float)) and r[column] < 0],
        "outliers_3sigma": [r["order_id"] for r in DATASET if isinstance(r.get(column), (int, float)) and sd > 0 and abs(r[column] - avg) > 3 * sd],
    }


def check_enum_values(column: str, allowed_values: list) -> dict:
    allowed = set(allowed_values)
    invalid = [{"order_id": r["order_id"], "value": r.get(column)} for r in DATASET if r.get(column) not in allowed]
    return {"invalid_count": len(invalid), "invalid_values": invalid}


def check_date_format(column: str) -> dict:
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    invalid = [{"order_id": r["order_id"], "value": r.get(column)} for r in DATASET
               if r.get(column) and not pattern.match(str(r[column]))]
    return {"invalid_count": len(invalid), "invalid_dates": invalid}


def dispatch(name: str, inp: dict):
    return {
        "check_nulls": lambda: check_nulls(),
        "check_duplicates": lambda: check_duplicates(),
        "check_value_ranges": lambda: check_value_ranges(inp["column"]),
        "check_enum_values": lambda: check_enum_values(inp["column"], inp["allowed_values"]),
        "check_date_format": lambda: check_date_format(inp["column"]),
        "submit_quality_report": lambda: inp,
    }[name]()


# ── Agent loop ────────────────────────────────────────────────────────────────
def run_quality_agent() -> dict:
    print(f"Running data quality agent on {len(DATASET)} records…\n")
    messages = [{"role": "user", "content": (
        f"Run a complete data quality assessment on this orders dataset ({len(DATASET)} records). "
        "Checks to run:\n"
        "1. check_nulls — all columns\n"
        "2. check_duplicates\n"
        "3. check_value_ranges for 'amount'\n"
        "4. check_enum_values for 'status' (allowed: completed, pending, refunded, cancelled)\n"
        "5. check_enum_values for 'region' (allowed: US, EU, APAC)\n"
        "6. check_date_format for 'date'\n"
        "Then submit_quality_report with all findings."
    )}]
    system = (
        "You are a data quality agent. Run ALL checks before submitting the report. "
        "Score: start at 100, deduct 15 per critical issue, 5 per warning, 1 per info. "
        "Severity: critical = data loss/corruption/PK violation, warning = invalid values/outliers, info = format issues."
    )

    while True:
        response = client.messages.create(
            model=MODEL, max_tokens=2048, system=system, tools=tools, messages=messages
        )
        if response.stop_reason == "end_turn":
            return {"narrative": next((b.text for b in response.content if hasattr(b, "text")), "")}
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  [{block.name}]")
                    result = dispatch(block.name, block.input)
                    if block.name == "submit_quality_report":
                        return result
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)})
            messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    report = run_quality_agent()
    print(f"\n{'='*60}\nDATA QUALITY REPORT\n{'='*60}")
    print(json.dumps(report, indent=2))
