# Module 01: Hands-On Exercises

## Exercise 1 — Quick (15 min): Connect an MCP Server

**Goal:** Experience connecting Claude to a real data system.

**What you need:** Claude Code installed, a PostgreSQL or SQLite database (local or dev)

**Steps:**
1. Create `.mcp.json` in a project directory:
```json
{
  "mcpServers": {
    "local-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "./sample.db"]
    }
  }
}
```
2. Create a small SQLite database:
```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('sample.db')
conn.execute('CREATE TABLE sales (id INTEGER, product TEXT, amount REAL, date TEXT)')
conn.execute('INSERT INTO sales VALUES (1,\"Widget\",150.0,\"2026-06-01\")')
conn.execute('INSERT INTO sales VALUES (2,\"Gadget\",75.5,\"2026-06-02\")')
conn.commit()
"
```
3. Open Claude Code in that directory and ask: *"What tables do I have and what's in them?"*

**What to observe:** Claude reads the schema and data via MCP — no tool was given by you. The MCP server handled connectivity automatically.

**Reflection:** What would this have required before MCP? (Manual schema description in the prompt, or a custom tool.)

---

## Exercise 2 — Medium (45 min): Build a Simple Agent

**Goal:** Write your first data agent from scratch using the pattern in `data-engineering/01-etl-pipeline-agent/main.py` as a reference.

**Task:** Build an agent that takes a list of CSV rows (in-memory), calculates summary stats (total, average, min, max for a numeric column), and returns a structured report.

**Starter structure:**
```python
import anthropic, json

client = anthropic.Anthropic()

DATA = [
    {"product": "Widget", "sales": 150},
    {"product": "Gadget", "sales": 75},
    {"product": "Doohickey", "sales": 220},
]

tools = [
    {
        "name": "calculate_stats",
        "description": "Calculate summary statistics for a numeric column. Returns min, max, mean, total.",
        "input_schema": {
            "type": "object",
            "properties": {
                "column": {"type": "string", "description": "Column name to compute stats for"}
            },
            "required": ["column"]
        }
    },
    # Add a submit_report tool here
]

# Implement the agent loop
# It should: call calculate_stats, then submit_report with findings
```

**Success criteria:**
- Agent correctly calls `calculate_stats` before `submit_report`
- Loop terminates on `stop_reason == "end_turn"` — not after a fixed number of turns
- Report is a structured dict, not free text

**Hint:** Look at how `05-ci-cd-automation/main.py` uses `tool_choice: {"type": "any"}` to force structured output.

---

## Exercise 3 — Deep (90 min): Map Your Stack to the 3-Layer Pattern

**Goal:** Audit your current workflow and produce a concrete plan for adding MCP + skills + agents.

**Step 1 — MCP audit (20 min):**
List every external system your pipelines touch. For each:
- Does an MCP server exist? (Check `references/tools-catalog.md`)
- What's the minimum permission scope needed?
- What would you NOT want Claude to be able to do via this MCP?

**Step 2 — Skills audit (15 min):**
List the things you explain to any AI assistant more than once per week. For each:
- Is this a reusable methodology? (Candidate for a skill)
- Is this project-specific context? (Goes in CLAUDE.md)
- Is this a one-time thing? (Just prompt it)

**Step 3 — Agent candidates (20 min):**
Look at Module 00's reflection exercise (most repetitive tasks). For each repetitive task:
- Does it have decision points, or is it always the same steps?
- If it has decision points → strong agent candidate
- If it's always the same → script with Claude calls at each step

**Step 4 — Write your plan (35 min):**
Produce a one-page document:
```
My current stack: [warehouse, transform, orchestration, DQ]

MCP servers to add:
- [system]: [MCP package] — scoped to [schemas/permissions]

Skills to create or install:
- [skill name]: [what it encodes]

Agent candidates:
- [task name]: [why it needs an agent vs a script]

First thing I'll build: [the one that would save me the most time]
```

This document becomes your personal roadmap for Modules 03 and 04.
