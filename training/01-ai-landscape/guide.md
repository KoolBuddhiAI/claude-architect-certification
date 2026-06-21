# Module 01: The AI Landscape — Reading Guide

## What This Module Is Really About

Most data engineers get lost in AI tooling because they try to understand all of it at once. This guide cuts it down to the three decisions that actually matter:

1. Does this task need to connect to an external system? → **MCP server**
2. Does this task follow a repeatable methodology I want Claude to learn? → **Skill**
3. Does this task require multi-step decisions to complete? → **Agent**

Everything else is detail.

---

## MCP Servers — The Connectivity Layer

An MCP (Model Context Protocol) server is a bridge. It lets Claude read from and write to systems it couldn't otherwise touch: your warehouse, your GitHub repos, your Jira board, your Fabric workspace.

**What makes a good MCP server decision:**

| Question | If Yes |
|---|---|
| Is the system external to Claude? | Candidate for MCP |
| Does it have a stable API? | Good MCP candidate |
| Is access sensitive / needs scoping? | Scope the MCP carefully |
| Will multiple workflows use it? | Worth the setup cost |

**The security rule nobody says loudly enough:** Every MCP server is a surface area. A Postgres MCP with full read/write on every schema is a risk. A Postgres MCP scoped to the `staging` and `analytics` schemas with INSERT/SELECT only is acceptable. Think of MCP permissions the same way you think about service account permissions.

**Practical setup:** See `references/mcp-servers.md` for copy-paste config for the most common data engineering systems.

---

## Skills — The Methodology Layer

A skill is procedural knowledge stored as a slash command. When you install a skill, you're teaching Claude how to do something the way your team does it — not just any way.

Skills are light (30–50 tokens each, loaded on demand). They don't connect to systems — that's what MCP servers do. They tell Claude *how to approach* a task.

**Data engineering skills worth knowing:**

- **BMAD skills** — planning methodology (Module 02 covers this deeply)
- **Data contract skill** — how to define a contract in your team's format
- **dbt model skill** — how to scaffold a dbt model following your conventions
- **Quality gate skill** — your standard DQ check definitions

**Writing your own skill:** A skill is essentially a well-written set of instructions in a markdown file. If you find yourself explaining the same thing to Claude in three different sessions, it belongs in a skill.

---

## Agents — The Execution Layer

An agent is Claude running in a loop with tools. The loop continues until the task is complete (`stop_reason == "end_turn"`) — not until a fixed number of steps, and not until you parse text from the response.

**The agent loop (simplified):**
```
System prompt + task
    ↓
Claude reasons: what tool do I need?
    ↓
Tool called → result returned
    ↓
Claude reasons: am I done?
    ├── No → call another tool
    └── Yes → end_turn
```

**When NOT to use an agent:**
- The task is linear and has no decision points → use a script
- The task is one step → just ask Claude directly
- You need guaranteed execution order → orchestrate the steps yourself

**The most common mistake:** Making everything an agent. An agent adds latency, cost, and unpredictability. Use it when the task genuinely requires reasoning about what to do next. For predictable multi-step tasks with no branching, a script calling Claude at each step is often better.

---

## How They Work Together

The 2026 pattern for data engineering:

```
Claude Code (your IDE)
    │
    ├── MCP Servers — connect to your data systems
    │   └── Postgres, Snowflake, Fabric, GitHub...
    │
    ├── Skills — encode your team's methodology
    │   └── BMAD, data contracts, dbt conventions...
    │
    └── Agents — execute complex multi-step tasks
        └── ETL pipelines, quality checks, SQL generation...
```

A typical data engineering workflow uses all three:
- MCP for the warehouse connection
- A skill for the data contract template
- An agent to implement the pipeline

None replaces the others. Each has a distinct job.

---

## Platform Choices

The patterns above work regardless of your warehouse. What changes is the MCP server:

| Your Stack | MCP Server | Notes |
|---|---|---|
| PostgreSQL | `@modelcontextprotocol/server-postgres` | Most common |
| Snowflake | `mcp-snowflake` | Community, actively maintained |
| Microsoft Fabric | `skills-for-fabric` | Official Microsoft package |
| BigQuery | ADK-native or BigQuery MCP | Google ADK preferred |
| SQLite (local dev) | `@modelcontextprotocol/server-sqlite` | Great for prototyping |

The agent code you write is portable. The MCP connection is not. But swapping MCP servers when you change databases takes minutes, not days.

---

## Before You Move On

You should be able to answer:

- [ ] What is the difference between an MCP server and a skill?
- [ ] When would you use an agent vs a direct Claude call?
- [ ] Why does `stop_reason == "end_turn"` matter for agent loops?
- [ ] What security consideration applies to every MCP server?
- [ ] What's the correct platform choice for your current stack?

**Coming up in Module 02:** Now that you know the building blocks, we'll cover how to plan a data engineering project using them properly — before any agent writes a line of code.
