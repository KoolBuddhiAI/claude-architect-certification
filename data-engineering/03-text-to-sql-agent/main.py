"""
Text-to-SQL Agent — Scenario DE-03
Demonstrates: runtime schema introspection, validation-retry loop, dry-run before execute.
Uses in-memory SQLite with a sample e-commerce schema.
"""
import anthropic
import json
import sqlite3

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

# ── Sample database setup ────────────────────────────────────────────────────
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

conn.executescript("""
    CREATE TABLE customers (
        id         TEXT PRIMARY KEY,
        name       TEXT NOT NULL,
        email      TEXT UNIQUE NOT NULL,
        region     TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE products (
        id       TEXT PRIMARY KEY,
        name     TEXT NOT NULL,
        category TEXT NOT NULL,
        price    REAL NOT NULL
    );
    CREATE TABLE orders (
        id           TEXT PRIMARY KEY,
        customer_id  TEXT NOT NULL REFERENCES customers(id),
        created_at   TEXT NOT NULL,
        status       TEXT NOT NULL,
        total_amount REAL NOT NULL
    );
    CREATE TABLE order_items (
        id         TEXT PRIMARY KEY,
        order_id   TEXT NOT NULL REFERENCES orders(id),
        product_id TEXT NOT NULL REFERENCES products(id),
        quantity   INTEGER NOT NULL,
        unit_price REAL NOT NULL
    );

    INSERT INTO customers VALUES
        ('C001','Alice Chen','alice@example.com','US','2026-01-15'),
        ('C002','Bob Smith','bob@example.com','EU','2026-02-20'),
        ('C003','Carol Wu','carol@example.com','APAC','2026-03-10'),
        ('C004','Dan Park','dan@example.com','US','2026-04-05');

    INSERT INTO products VALUES
        ('P001','Laptop Pro 14','Electronics',1299.99),
        ('P002','Wireless Mouse','Electronics',49.99),
        ('P003','Desk Lamp','Office',34.99),
        ('P004','Standing Desk','Office',449.99);

    INSERT INTO orders VALUES
        ('ORD-001','C001','2026-06-01','completed',1349.98),
        ('ORD-002','C002','2026-06-05','completed',449.99),
        ('ORD-003','C001','2026-06-10','pending',34.99),
        ('ORD-004','C003','2026-06-12','completed',1299.99),
        ('ORD-005','C004','2026-06-15','refunded',49.99);

    INSERT INTO order_items VALUES
        ('OI-001','ORD-001','P001',1,1299.99),
        ('OI-002','ORD-001','P002',1,49.99),
        ('OI-003','ORD-002','P004',1,449.99),
        ('OI-004','ORD-003','P003',1,34.99),
        ('OI-005','ORD-004','P001',1,1299.99),
        ('OI-006','ORD-005','P002',1,49.99);
""")
conn.commit()

# ── Tool definitions ─────────────────────────────────────────────────────────
tools = [
    {
        "name": "get_schema",
        "description": (
            "Retrieve the live database schema: all table names, column names, types, and constraints. "
            "Always call this FIRST before writing any SQL."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "validate_sql",
        "description": (
            "Dry-run a SQL query using EXPLAIN QUERY PLAN — no data modification. "
            "Catches syntax errors, missing tables/columns, and bad JOIN conditions. "
            "Always call before execute_sql."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"sql": {"type": "string", "description": "SQL query to validate"}},
            "required": ["sql"],
        },
    },
    {
        "name": "execute_sql",
        "description": (
            "Execute a validated SELECT query and return results as JSON. "
            "Limited to 100 rows. Only call after validate_sql confirms the query is valid."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "Validated SELECT query to execute"},
                "description": {"type": "string", "description": "What this query answers"},
            },
            "required": ["sql", "description"],
        },
    },
]


# ── Tool implementations ──────────────────────────────────────────────────────
def get_schema() -> dict:
    tables = {}
    for (table,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
        cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
        fks = conn.execute(f"PRAGMA foreign_key_list({table})").fetchall()
        tables[table] = {
            "columns": [{"name": c[1], "type": c[2], "not_null": bool(c[3]), "pk": bool(c[5])} for c in cols],
            "foreign_keys": [{"column": f[3], "references": f"{f[2]}({f[4])}"} for f in fks],
        }
    return {"tables": tables}


def validate_sql(sql: str) -> dict:
    try:
        conn.execute(f"EXPLAIN QUERY PLAN {sql}")
        return {"valid": True}
    except sqlite3.Error as e:
        return {"valid": False, "error": str(e)}


def execute_sql(sql: str, description: str) -> dict:
    try:
        cursor = conn.execute(sql + (" LIMIT 100" if "LIMIT" not in sql.upper() else ""))
        cols = [d[0] for d in cursor.description]
        rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
        return {"description": description, "column_names": cols, "rows": rows, "row_count": len(rows)}
    except sqlite3.Error as e:
        return {"error": str(e)}


def dispatch(name: str, inp: dict):
    return {
        "get_schema": lambda: get_schema(),
        "validate_sql": lambda: validate_sql(inp["sql"]),
        "execute_sql": lambda: execute_sql(inp["sql"], inp.get("description", "")),
    }[name]()


# ── Agent loop with validation-retry ─────────────────────────────────────────
def ask(question: str, max_retries: int = 3) -> dict:
    print(f"\nQuestion: {question}")
    messages = [{"role": "user", "content": question}]
    system = (
        "You are a Text-to-SQL agent. Workflow for every question:\n"
        "1. get_schema — fetch the live schema first\n"
        "2. validate_sql — dry-run your SQL before executing\n"
        "3. If validate_sql returns valid=false, fix the SQL and validate again (max 3 attempts)\n"
        "4. execute_sql — only after validation passes\n"
        "Write standard SQL compatible with SQLite. Use table aliases for clarity."
    )
    retry_count = 0

    while True:
        response = client.messages.create(
            model=MODEL, max_tokens=2048, system=system, tools=tools, messages=messages
        )
        if response.stop_reason == "end_turn":
            return {"answer": next((b.text for b in response.content if hasattr(b, "text")), ""), "retries": retry_count}
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = dispatch(block.name, block.input)
                    print(f"  [{block.name}]", "✓" if result.get("valid", True) and "error" not in result else f"✗ {result.get('error','')}")
                    if block.name == "validate_sql" and not result.get("valid"):
                        retry_count += 1
                        if retry_count >= max_retries:
                            result["note"] = f"Max retries ({max_retries}) reached"
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)})
            messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    questions = [
        "How many orders did each customer place, and what was their total spend?",
        "What are the top 2 products by total quantity sold?",
        "Which customers placed an order in June 2026 that has 'completed' status?",
    ]
    for q in questions:
        result = ask(q)
        print(f"  Answer: {result['answer'][:200]}{'...' if len(result['answer']) > 200 else ''}")
        if result["retries"]:
            print(f"  (required {result['retries']} SQL retries)")
        print()
