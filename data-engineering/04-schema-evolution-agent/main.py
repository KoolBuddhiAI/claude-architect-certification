"""
Schema Evolution Agent — Scenario DE-04
Demonstrates: schema diffing, breaking/non-breaking classification, migration SQL generation.
"""
import anthropic
import json

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

# ── Schema versions ───────────────────────────────────────────────────────────
SCHEMA_V1 = {
    "orders": {
        "columns": [
            {"name": "id",          "type": "TEXT",           "nullable": False, "primary_key": True},
            {"name": "customer_id", "type": "TEXT",           "nullable": False},
            {"name": "total",       "type": "DECIMAL(10,2)",  "nullable": False},
            {"name": "legacy_ref",  "type": "TEXT",           "nullable": True},   # will be removed
            {"name": "status",      "type": "VARCHAR(20)",    "nullable": False},
            {"name": "created_at",  "type": "TIMESTAMP",      "nullable": False},
        ]
    },
    "customers": {
        "columns": [
            {"name": "id",         "type": "TEXT",        "nullable": False, "primary_key": True},
            {"name": "name",       "type": "TEXT",        "nullable": False},
            {"name": "email",      "type": "TEXT",        "nullable": False},
            {"name": "phone",      "type": "VARCHAR(15)", "nullable": True},   # type will widen
        ]
    },
    "products": {
        "columns": [
            {"name": "id",    "type": "TEXT", "nullable": False, "primary_key": True},
            {"name": "name",  "type": "TEXT", "nullable": False},
            {"name": "price", "type": "REAL", "nullable": False},
            # sku will be added as NOT NULL (breaking)
        ]
    },
}

SCHEMA_V2 = {
    "orders": {
        "columns": [
            {"name": "id",               "type": "TEXT",          "nullable": False, "primary_key": True},
            {"name": "customer_id",      "type": "TEXT",          "nullable": False},
            {"name": "total",            "type": "DECIMAL(10,2)", "nullable": False},
            # legacy_ref removed
            {"name": "discount_amount",  "type": "DECIMAL(10,2)", "nullable": True},   # new nullable col
            {"name": "status",           "type": "VARCHAR(20)",   "nullable": False},
            {"name": "created_at",       "type": "TIMESTAMP",     "nullable": False},
        ]
    },
    "customers": {
        "columns": [
            {"name": "id",    "type": "TEXT",        "nullable": False, "primary_key": True},
            {"name": "name",  "type": "TEXT",        "nullable": False},
            {"name": "email", "type": "TEXT",        "nullable": False},
            {"name": "phone", "type": "VARCHAR(20)", "nullable": True},   # widened from 15→20
        ]
    },
    "products": {
        "columns": [
            {"name": "id",    "type": "TEXT",        "nullable": False, "primary_key": True},
            {"name": "name",  "type": "TEXT",        "nullable": False},
            {"name": "price", "type": "REAL",        "nullable": False},
            {"name": "sku",   "type": "VARCHAR(50)", "nullable": False},  # NOT NULL without default — breaking
        ]
    },
    "promotions": {   # new table (non-breaking)
        "columns": [
            {"name": "id",         "type": "TEXT",          "nullable": False, "primary_key": True},
            {"name": "code",       "type": "VARCHAR(20)",   "nullable": False},
            {"name": "discount",   "type": "DECIMAL(5,2)",  "nullable": False},
            {"name": "expires_at", "type": "TIMESTAMP",     "nullable": True},
        ]
    },
}

# ── Tool definitions ─────────────────────────────────────────────────────────
tools = [
    {
        "name": "diff_schemas",
        "description": (
            "Compare V1 and V2 schemas and return a structured diff: "
            "new tables, removed tables, per-table added/removed/modified columns. "
            "Returns raw change list — classification happens in classify_changes."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "classify_changes",
        "description": (
            "Classify each detected change as 'breaking' or 'non_breaking'. "
            "Breaking: column removal, NOT NULL addition without default, type narrowing, rename. "
            "Non-breaking: add nullable column, type widening, add new table, add index. "
            "Input: the diff output from diff_schemas."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"diff": {"type": "object", "description": "Output from diff_schemas"}},
            "required": ["diff"],
        },
    },
    {
        "name": "submit_migration_plan",
        "description": "Submit the complete migration plan after diffing and classifying all changes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "deployment_risk": {"type": "string", "enum": ["low", "medium", "high"]},
                "changes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "table": {"type": "string"},
                            "change_type": {"type": "string"},
                            "classification": {"type": "string", "enum": ["breaking", "non_breaking"]},
                            "description": {"type": "string"},
                        },
                        "required": ["table", "change_type", "classification", "description"],
                    },
                },
                "forward_sql": {"type": "array", "items": {"type": "string"}, "description": "Ordered migration SQL statements"},
                "rollback_sql": {"type": "array", "items": {"type": "string"}, "description": "Ordered rollback SQL statements"},
                "pre_deployment_checklist": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["deployment_risk", "changes", "forward_sql", "rollback_sql", "pre_deployment_checklist"],
        },
    },
]


# ── Tool implementations ──────────────────────────────────────────────────────
def diff_schemas() -> dict:
    v1_tables, v2_tables = set(SCHEMA_V1), set(SCHEMA_V2)
    result = {
        "new_tables": list(v2_tables - v1_tables),
        "removed_tables": list(v1_tables - v2_tables),
        "modified_tables": {},
    }
    for table in v1_tables & v2_tables:
        v1_cols = {c["name"]: c for c in SCHEMA_V1[table]["columns"]}
        v2_cols = {c["name"]: c for c in SCHEMA_V2[table]["columns"]}
        added = [v2_cols[n] for n in set(v2_cols) - set(v1_cols)]
        removed = [v1_cols[n] for n in set(v1_cols) - set(v2_cols)]
        modified = [
            {"name": n, "v1": v1_cols[n], "v2": v2_cols[n]}
            for n in set(v1_cols) & set(v2_cols)
            if v1_cols[n] != v2_cols[n]
        ]
        if added or removed or modified:
            result["modified_tables"][table] = {"added": added, "removed": removed, "modified": modified}
    return result


def classify_changes(diff: dict) -> dict:
    classifications = []
    for table in diff.get("new_tables", []):
        classifications.append({"table": table, "change": "new table", "breaking": False})
    for table in diff.get("removed_tables", []):
        classifications.append({"table": table, "change": "table removed", "breaking": True})
    for table, changes in diff.get("modified_tables", {}).items():
        for col in changes.get("added", []):
            breaking = not col.get("nullable", True)  # NOT NULL without default = breaking
            classifications.append({"table": table, "change": f"add column {col['name']}", "breaking": breaking,
                                     "note": "NOT NULL without default — requires two-step migration" if breaking else None})
        for col in changes.get("removed", []):
            classifications.append({"table": table, "change": f"drop column {col['name']}", "breaking": True})
        for mod in changes.get("modified", []):
            v1t, v2t = mod["v1"]["type"], mod["v2"]["type"]
            widening = ("VARCHAR(15)" in v1t and "VARCHAR(20)" in v2t) or ("INT" in v1t and "BIGINT" in v2t)
            classifications.append({"table": table, "change": f"modify column {mod['name']}: {v1t}→{v2t}",
                                     "breaking": not widening})
    return {"classifications": classifications, "has_breaking_changes": any(c["breaking"] for c in classifications)}


def dispatch(name: str, inp: dict):
    return {
        "diff_schemas": lambda: diff_schemas(),
        "classify_changes": lambda: classify_changes(inp["diff"]),
        "submit_migration_plan": lambda: inp,
    }[name]()


# ── Agent loop ────────────────────────────────────────────────────────────────
def run_schema_evolution_agent() -> dict:
    print("Analyzing schema evolution V1 → V2…\n")
    messages = [{
        "role": "user",
        "content": (
            "Analyze the schema evolution from V1 to V2. Steps:\n"
            "1. diff_schemas — get the raw change list\n"
            "2. classify_changes — classify each change as breaking or non-breaking\n"
            "3. submit_migration_plan — with forward SQL, rollback SQL, and a pre-deployment checklist\n\n"
            "For breaking changes, generate safe multi-step migrations:\n"
            "- Adding NOT NULL column: (1) add nullable, (2) UPDATE to set default, (3) add NOT NULL constraint\n"
            "- Dropping column: include rollback SQL to restore it"
        ),
    }]
    system = (
        "You are a database schema evolution agent. "
        "Run diff → classify → submit_migration_plan in order. "
        "Generate complete, executable SQL for both forward migration and rollback. "
        "Deployment risk: 'high' if any breaking changes exist, 'medium' if warnings, 'low' otherwise."
    )

    while True:
        response = client.messages.create(
            model=MODEL, max_tokens=4096, system=system, tools=tools, messages=messages
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
                    if block.name == "submit_migration_plan":
                        return result
                    results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)})
            messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    plan = run_schema_evolution_agent()
    print(f"\n{'='*60}\nMIGRATION PLAN\n{'='*60}")
    print(json.dumps(plan, indent=2))
