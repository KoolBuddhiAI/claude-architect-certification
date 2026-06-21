# Google ADK Patterns for Data Engineering
## Extracted from "How to Build a Data Science Agent with ADK" (Google Hands-On with AI Agents)

Source: YouTube transcript — Google ADK team demo (Melam + SA)

---

## Architecture: Data Science Multi-Agent System

The ADK data science agent is built as a **root agent + two agent tools + one sub-agent**:

```
Root Agent (data agent — user-facing)
├── Database Agent      → agent-as-tool   (SQL generation + BigQuery execution)
├── Data Science Agent  → agent-as-tool   (NL2Python, plots, analysis)
└── BQML Agent          → sub-agent       (full session transfer for ML workloads)
```

Each agent follows the same file structure:
```
agent_name/
├── agent.py          # ADK Agent class instantiation + config
├── instructions.py   # Prompts outsourced here (iterate without touching logic)
└── tools.py          # All tools for this agent
```

---

## Key Distinction: Agent-as-Tool vs Sub-Agent

This is the most important architectural decision in the ADK multi-agent pattern:

### Agent-as-Tool
- Root agent **delegates a task** → tool agent completes it → **always returns to root**
- User continues their session with the **root agent**
- Best for: query-response patterns (SQL fetch, data analysis, one-shot tasks)

```python
# Example: DB agent as a tool
root_agent = Agent(
    tools=[call_db_agent, call_ds_agent, load_artifacts],  # agents provided as tools
    sub_agents=[bqml_agent]  # sub-agent for session transfer
)
```

### Sub-Agent (Session Transfer)
- Root agent **transfers the full conversation** to the sub-agent
- User is now **talking directly with the sub-agent**
- Can transfer back to root when the sub-agent detects the topic changes
- Best for: extended multi-turn workflows (model training, iterative ML sessions)

**Why BQML is a sub-agent**: BigQuery ML training involves multiple back-and-forth turns. Forcing the user to relay through the root agent every turn would be awkward. Session transfer lets the BQML agent own the full ML training conversation.

---

## Before/After Agent Callbacks

ADK provides `before_agent_call` and `after_agent_call` hooks on **every agent** (root and sub-agents):

```python
def setup_before_agent_call(callback_context):
    # Runs BEFORE the agent loop starts — deterministic pre-setup
    # Example: inject BigQuery schema + DDL into context
    bq_settings = get_bigquery_database_settings()  # tool call
    callback_context.state["db_settings"] = bq_settings
    callback_context.state["bq_ddl_schema"] = bq_settings.ddl_schema
```

**Why this matters**: Schema injection via callback is **more deterministic** than schema-as-tool:
- With `get_schema` tool: agent decides *when* (or whether) to call it
- With `before_agent_call`: schema is **always** injected before every turn — guaranteed

The root agent can answer schema questions instantly (no tool call, no latency) because the DDL is pre-loaded into context.

**Use for**: any context that should *always* be available — today's date, user permissions, dataset metadata, feature flags.

---

## Global Instruction vs Instruction

```python
root_agent = Agent(
    instruction=ROOT_AGENT_INSTRUCTIONS,     # only this agent sees this
    global_instruction=f"Today's date: {today}",  # ALL sub-agents inherit this
)
```

- `instruction`: scoped to **this agent only** — sub-agents cannot see it
- `global_instruction`: inherited by **all sub-agents** — keep it minimal and factual

**Pattern**: Use `global_instruction` only for universal facts (date, user ID, dataset name). Put domain-specific workflow instructions in each agent's own `instruction`.

---

## Tool Context: Short-Term Shared Memory

Tool context persists **within a session** across all tool calls — including cross-agent calls:

```python
# In DB agent tool:
async def call_db_agent(question: str, tool_context: ToolContext):
    result = await db_agent_tool.run_async(request=question, tool_context=tool_context)
    
    # Store result in tool context for other agents to access
    tool_context.state["db_agent_output"] = result.text
    tool_context.state["last_sql"] = result.sql
    return result

# In DS agent tool — can now access DB agent's output:
async def call_ds_agent(question: str, tool_context: ToolContext):
    db_data = tool_context.state.get("db_agent_output", "")
    
    request = f"Question: {question}\nData from database:\n{db_data}"
    result = await ds_agent_tool.run_async(request=request, tool_context=tool_context)
    return result
```

**Key insight**: The DS agent never re-fetches data the DB agent already retrieved. Tool context acts as **shared working memory** for the session — avoiding redundant API calls.

---

## SQL Validation + Retry (Database Agent)

The database agent has a built-in **SQL validator and fixer**:

```
User query
    ↓
Generate SQL (Gemini native or JSQL method)
    ↓
Validate SQL syntax
    ↓ (if error)
Auto-fix SQL with error context
    ↓
Execute against BigQuery
    ↓
Return data + SQL to root agent
```

Two SQL generation methods available (switchable via `.env`):
1. **Native Gemini**: Standard LLM SQL generation — good for most cases
2. **JSQL** (from Google Cloud AI research): Research method, top-5 on BIRD SQL benchmark — better for complex queries

---

## Instructions File Pattern

Outsource prompts to `instructions.py` to:
- Iterate on prompts without touching agent logic
- Keep version history of prompt variants
- Make prompt tuning fast and isolated

**Prompt quality rules from the ADK team:**
1. Human readable — if you can't understand it, the LLM can't either
2. No contradictions
3. Define workflow order explicitly: "First call DB agent, then DS agent"
4. Make conditional calls explicit: "If the user asks for ML workloads, transfer to BQML"

---

## ADK Built-in Tooling

| ADK Feature | What It Does |
|---|---|
| `load_artifacts` | Manages generated artifacts (plots, files) across multi-agent session |
| `adk web` | Spins up a local Angular dev frontend — no streaming or UI code needed |
| `AgentEvaluator` | Create eval sets from sessions, run regression tests after changes |
| Code interpreter extension | Execute Python code for NL2Python (plots, statistical analysis) |
| RAG tool | Built-in retrieval for Vertex AI Search / Vertex AI RAG |

---

## Extending the Architecture

Adding a new agent to the system:

```python
# 1. Create your agent
new_agent = Agent(
    model="gemini-2.0-flash",
    name="new_specialist_agent",
    instruction=NEW_AGENT_INSTRUCTIONS,
    tools=[your_tools],
)

# 2a. Add as tool (query-response pattern)
root_agent = Agent(
    tools=[..., AgentTool(agent=new_agent)],
)

# 2b. Add as sub-agent (session transfer pattern)
root_agent = Agent(
    sub_agents=[..., new_agent],
)
```

The ADK handles routing automatically. The root agent's prompt specifies when to call each agent/sub-agent.

---

## Evaluation Framework

ADK has a built-in evaluation tab in the web UI:

```python
# Create eval set from a session
evaluator = AgentEvaluator()
eval_set = evaluator.create_from_session(session_id)

# Run regression tests after changes
results = evaluator.run(agent, eval_set, threshold=0.95)
```

Also integrated with BIRD SQL benchmark for NL2SQL evaluation. The data science agent sample achieved **top-5 on BIRD SQL benchmark** using the JSQL method.

---

## Applying ADK Patterns to Your Stack (Non-GCP)

The ADK is GCP/Gemini-native but the **patterns translate directly to Claude**:

| ADK Concept | Claude Equivalent |
|---|---|
| `before_agent_call` callback | Inject schema via `cache_control` system prompt or first tool call |
| `global_instruction` | Shared prefix in system prompt |
| `instruction` per agent | Agent-specific system prompt |
| Tool context state | Explicit context passing in tool results |
| Agent-as-tool | Claude orchestrator calling subagent and returning result |
| Sub-agent (session transfer) | Full conversation handoff to specialist Claude instance |
| `adk web` | Claude Code interactive session |
| `AgentEvaluator` | Custom eval harness with `anthropic.messages.create` |
