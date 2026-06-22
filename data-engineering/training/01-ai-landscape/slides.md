---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
---

# "What even is all of this?"

*Cutting through the noise on agents, skills, and MCP*

*Module 01 · AI-Native Data Engineering*

---

# You've probably seen the hype

"Agents!" "MCP servers!" "Skills!" "Agentic workflows!"

And thought: *what does any of this actually mean for my job?*

Fair question. Let's make it concrete.

By the end of this module you'll know exactly what each piece is, when to use it, and — more importantly — when **not** to bother.

---

# Three Building Blocks

```
┌─────────────────────────────────────────────┐
│                                             │
│   MCP Servers    →  Connectivity            │
│   Skills         →  Methodology             │
│   Agents         →  Execution               │
│                                             │
└─────────────────────────────────────────────┘
```

These are not interchangeable. Choosing the wrong one for the job is the most common mistake.

---

# MCP Servers — Connectivity Layer

**What they are**: Bridges between Claude and external systems

**What they do**: Give Claude the ability to READ and WRITE to databases, APIs, and services

**Data engineering examples:**
- `@modelcontextprotocol/server-postgres` → Query your warehouse
- `skills-for-fabric` → Access Fabric/Power BI directly
- `@modelcontextprotocol/server-github` → Read/write your repos
- BigQuery MCP → Query and manage BigQuery datasets

**Rule**: One MCP server per external system. Pin versions. Scope access to least privilege.

---

# Skills — Methodology Layer

**What they are**: Procedural knowledge stored as slash commands (~30–50 tokens each)

**What they do**: Teach Claude HOW to do something in your context

**Data engineering examples:**
- `/bmad-architecture` → How to design a data architecture
- `/dbt-model` → How to scaffold a dbt model for your project conventions
- `/data-contract` → How to define a data contract using your template

**Rule**: One skill per repeatable methodology. Load on-demand, not always.

**Key insight**: Skills ≠ tools. Skills are instructions. MCP servers are connections.

---

# Agents — Execution Layer

**What they are**: Claude instances running in a loop, using tools to complete multi-step tasks

**What they do**: Execute complex, non-linear workflows autonomously

**Data engineering examples:**
- ETL pipeline agent: fetch → transform → validate → load
- Data quality agent: run checks → classify → report → gate
- Schema evolution agent: diff → classify → generate migration → validate

**Rule**: Use agents when the path to completion requires decisions along the way. For linear scripts, use Skills.

---

# The Decision Tree

```
Does the task need real-time access to an external system?
    YES → MCP Server
    NO  ↓

Does the task follow a known methodology Claude should learn?
    YES → Skill
    NO  ↓

Does the task require multi-step decision-making?
    YES → Agent
    NO  ↓

Just ask Claude directly (no scaffolding needed)
```

---

# Platform Overview: Anthropic

| Component | Purpose | Data Engineering Use |
|---|---|---|
| Claude API | Raw model access | Build custom DE agents |
| Claude Code | IDE for agentic work | Your daily driver |
| MCP protocol | Connectivity standard | Connect to every data store |
| Skills marketplace | Community methodology | Install proven workflows |
| Agent SDK | Multi-agent orchestration | Pipeline orchestration |

**Claude Code is the data engineer's primary workbench in 2026.**

---

# Platform Overview: Microsoft Fabric

| Component | Purpose |
|---|---|
| `fabric-authoring` skill | Create pipelines, notebooks, semantic models |
| `fabric-consumption` skill | Query warehouses, lakehouses, Power BI |
| `fabric-operations` skill | Diagnose performance, slow queries |
| `powerbi-authoring` skill | Author PBIR reports, publish, iterate |
| Fabric MCP server | Direct API access to all Fabric workloads |

**Migration path**: Power BI Q&A retires Dec 2026. Claude + Fabric MCP is the replacement.

---

# Platform Overview: Google Cloud (ADK)

| Component | Purpose |
|---|---|
| Google ADK | Open-source agent framework (Python/TS/Go/Java) |
| ADK data-engineering sample | Dataform pipeline ownership agent |
| AgentEvaluator | Test-first validation of agent responses |
| Vertex AI | Model backend for ADK agents |
| BigQuery MCP | Query and manage BigQuery datasets |

**ADK thesis**: Agents own Dataform workspaces end-to-end — not just SQL snippets.

---

# Platform Overview: Community

| Tool | What It Provides |
|---|---|
| **BMAD Method** | 20 slash commands for agile AI-driven development |
| **Superpowers** | Full dev lifecycle framework (40.9k ⭐) |
| `awesome-claude-code-subagents` | Community agent library |
| dbt + Claude | Schema-aware model generation |
| Great Expectations MCP | Data quality as code |

**Pattern**: Pin one MCP per data system + use proven skills for methodology.

---

# Choosing Your Stack — Decision Guide

| Situation | Recommended Approach |
|---|---|
| Team uses Microsoft Fabric / Power BI | `skills-for-fabric` + Claude Code |
| Team uses BigQuery / GCP | Google ADK + BigQuery MCP |
| Team uses Snowflake / dbt | Snowflake MCP + dbt skills |
| Team uses Postgres / custom stack | Postgres MCP + custom skills |
| Mixed / cloud-agnostic | Anthropic SDK agents + MCP per system |

**The model is platform-agnostic. The MCP servers are not.**

---

# The 2026 Stack for a Data Engineer

```
Claude Code (IDE)
    │
    ├── MCP Servers (connectivity)
    │   ├── Postgres / Snowflake / BigQuery / Fabric
    │   ├── GitHub (code)
    │   └── Jira / Linear (tickets)
    │
    ├── Skills (methodology)
    │   ├── BMAD or Superpowers (planning)
    │   ├── Data contract template
    │   └── Quality gate definitions
    │
    └── Custom Agents (execution)
        ├── ETL pipeline agent
        ├── Data quality agent
        └── Text-to-SQL agent
```

---

# What to Avoid

| Anti-Pattern | Why It Fails |
|---|---|
| One massive MCP server for everything | Too broad, security risk, hard to debug |
| Embedding schema in system prompts | Goes stale immediately |
| No skill methodology — just prompting | Inconsistent outputs, no team standards |
| Agents without quality gates | Silent failures reach production |
| Skipping AgentEvaluator / evals | No way to know if agents regressed |

---

# Module 01 — Key Takeaways

- **MCP** = connectivity to systems (one per system, least privilege)
- **Skills** = methodology (what Claude knows about your way of working)
- **Agents** = execution (multi-step, decision-making loops)
- Platform choice is secondary — the **patterns are the same** across Fabric, ADK, and raw Anthropic API
- Claude Code is your primary interface — learn it deeply

**Next: Module 02 — BMAD for Data Engineering**
