"""
ETL Pipeline Agent — Scenario DE-01
Demonstrates: stage-as-tool pattern, error-as-data, pagination, deduplication.
Uses in-memory SQLite as the target warehouse.
"""
import anthropic
import json
import sqlite3
from datetime import datetime, timezone

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

# ── Simulated paginated source API ──────────────────────────────────────────
MOCK_PAGES = [
    [
        {"id": "inv_001", "customer": {"id": "C001", "name": "Acme Corp"}, "amount_cents": 150000, "currency": "usd", "status": "paid", "created": "2026-06-01T10:00:00Z"},
        {"id": "inv_002", "customer": {"id": "C002", "name": "Widget Co"}, "amount_cents": 75000, "currency": "usd", "status": "open", "created": "2026-06-02T14:30:00Z"},
        {"id": "inv_003", "customer": {"id": "C001", "name": "Acme Corp"}, "amount_cents": None, "currency": "usd", "status": "draft", "created": "2026-06-03T09:00:00Z"},  # bad: null amount
    ],
    [
        {"id": "inv_004", "customer": {"id": "C003", "name": "TechStart"}, "amount_cents": 22000, "currency": "eur", "status": "paid", "created": "2026-06-04T16:00:00Z"},
        {"id": "inv_001", "customer": {"id": "C001", "name": "Acme Corp"}, "amount_cents": 150000, "currency": "usd", "status": "paid", "created": "2026-06-01T10:00:00Z"},  # duplicate
    ],
]

# ── Target warehouse (in-memory SQLite) ──────────────────────────────────────
conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE invoices (
        id           TEXT PRIMARY KEY,
        customer_id  TEXT NOT NULL,
        customer_name TEXT NOT NULL,
        amount_usd   REAL NOT NULL,
        currency     TEXT NOT NULL,
        status       TEXT NOT NULL,
        created_at   TEXT NOT NULL,
        loaded_at    TEXT NOT NULL
    )
""")
conn.commit()
_loaded_ids: set[str] = set()

# ── Tool definitions ─────────────────────────────────────────────────────────
tools = [
    {
        "name": "fetch_page",
        "description": (
            "Fetch one page of invoice records from the source API. "
            "Returns: records (list), has_more (bool), total_pages (int). "
            "Start at page=0 and increment until has_more is false."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"page": {"type": "integer", "description": "Zero-based page index"}},
            "required": ["page"],
        },
    },
    {
        "name": "transform_record",
        "description": (
            "Transform one raw API record into the flat warehouse schema. "
            "Validates required fields, flattens customer object, converts amount_cents→USD (EUR×1.08). "
            "Returns transformed record OR {error: str, record_id: str} — never raises exceptions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"record": {"type": "object", "description": "Raw record from fetch_page"}},
            "required": ["record"],
        },
    },
    {
        "name": "load_records",
        "description": (
            "Bulk-load a batch of transformed records into the warehouse. "
            "Skips records with an 'error' key. Deduplicates by primary key id. "
            "Returns: {inserted, skipped_duplicates, failed} — call once per page."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "records": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Mix of transformed records and error objects from transform_record",
                }
            },
            "required": ["records"],
        },
    },
    {
        "name": "get_load_stats",
        "description": "Return final pipeline stats: total rows loaded, total USD amount, sample rows. Call once at the end.",
        "input_schema": {"type": "object", "properties": {}},
    },
]


# ── Tool implementations ──────────────────────────────────────────────────────
def fetch_page(page: int) -> dict:
    if page < len(MOCK_PAGES):
        return {"records": MOCK_PAGES[page], "has_more": page < len(MOCK_PAGES) - 1, "total_pages": len(MOCK_PAGES)}
    return {"records": [], "has_more": False, "total_pages": len(MOCK_PAGES)}


def transform_record(record: dict) -> dict:
    if record.get("amount_cents") is None:
        return {"error": "amount_cents is null", "record_id": record.get("id", "unknown")}
    try:
        rate = 1.08 if record["currency"] == "eur" else 1.0
        return {
            "id": record["id"],
            "customer_id": record["customer"]["id"],
            "customer_name": record["customer"]["name"],
            "amount_usd": round(record["amount_cents"] / 100 * rate, 2),
            "currency": record["currency"],
            "status": record["status"],
            "created_at": record["created"],
            "loaded_at": datetime.now(timezone.utc).isoformat(),
        }
    except (KeyError, TypeError) as exc:
        return {"error": str(exc), "record_id": record.get("id", "unknown")}


def load_records(records: list) -> dict:
    inserted = skipped = failed = 0
    for rec in records:
        if "error" in rec:
            failed += 1
            continue
        if rec["id"] in _loaded_ids:
            skipped += 1
            continue
        try:
            conn.execute(
                "INSERT INTO invoices VALUES (?,?,?,?,?,?,?,?)",
                (rec["id"], rec["customer_id"], rec["customer_name"],
                 rec["amount_usd"], rec["currency"], rec["status"],
                 rec["created_at"], rec["loaded_at"]),
            )
            conn.commit()
            _loaded_ids.add(rec["id"])
            inserted += 1
        except Exception:
            failed += 1
    return {"inserted": inserted, "skipped_duplicates": skipped, "failed": failed}


def get_load_stats() -> dict:
    total, amount = conn.execute("SELECT COUNT(*), SUM(amount_usd) FROM invoices").fetchone()
    sample = conn.execute("SELECT id, customer_name, amount_usd, status FROM invoices LIMIT 3").fetchall()
    return {
        "total_rows": total,
        "total_amount_usd": round(amount or 0, 2),
        "sample": [{"id": r[0], "customer": r[1], "amount_usd": r[2], "status": r[3]} for r in sample],
    }


def dispatch(name: str, inp: dict) -> dict:
    return {"fetch_page": lambda: fetch_page(inp["page"]),
            "transform_record": lambda: transform_record(inp["record"]),
            "load_records": lambda: load_records(inp["records"]),
            "get_load_stats": lambda: get_load_stats()}[name]()


# ── Agent loop ────────────────────────────────────────────────────────────────
def run_etl_agent() -> str:
    print("Starting ETL pipeline agent…\n")
    messages = [{"role": "user", "content": (
        "Run the full ETL pipeline: fetch all pages (start page=0, loop while has_more=true), "
        "transform each record individually, load as a batch after each page, "
        "then call get_load_stats and report the final results."
    )}]
    system = (
        "You are an ETL pipeline agent. Execute extract → transform → load sequentially per page.\n"
        "Rules:\n"
        "- Fetch page 0 first, then increment until has_more=false\n"
        "- Transform every record individually using transform_record\n"
        "- Load the full page batch in one load_records call (include both good and error records)\n"
        "- Never abort on a single record failure — the load tool handles errors gracefully\n"
        "- Call get_load_stats at the end before reporting"
    )

    while True:
        response = client.messages.create(
            model=MODEL, max_tokens=2048, system=system, tools=tools, messages=messages
        )
        if response.stop_reason == "end_turn":
            return next((b.text for b in response.content if hasattr(b, "text")), "")
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  [{block.name}] {json.dumps(block.input)[:80]}")
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(dispatch(block.name, block.input)),
                    })
            messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    summary = run_etl_agent()
    print(f"\n{'='*60}\n{summary}")
