# Module 04: Hands-On Exercises

## Exercise 1 — Quick (20 min): Tool Audit

**Goal:** Score every tool in your current stack for AI-native compatibility.

For each tool you use (warehouse, transform, orchestration, DQ, catalog, infra):

| Tool | MCP? | SDK? | Structured output? | CLI? | Claude trained? | Score |
|------|------|------|--------------------|------|-----------------|-------|
| [your warehouse] | | | | | | /5 |
| [your transform] | | | | | | /5 |
| [your orchestration] | | | | | | /5 |
| [your DQ tool] | | | | | | /5 |

Use `references/tools-catalog.md` to check MCP availability.

**Reflection:** Which tool in your stack has the lowest score? That's either a gap to fill (find/build an MCP) or a candidate for replacement.

---

## Exercise 2 — Medium (45 min): Set Up Your MCP Stack

**Goal:** Get your two most important data systems connected to Claude Code via MCP.

**Step 1:** Choose your two priority systems (warehouse + GitHub are a good starting pair).

**Step 2:** Create `.mcp.json` using the templates in `references/mcp-servers.md`. Scope permissions to the minimum needed.

**Step 3:** Open Claude Code and verify the connection:
- For database MCP: "What tables exist in the [schema] schema?"
- For GitHub MCP: "List the last 5 commits on main."

**Step 4:** Verify security scoping:
- For database: try a query on a schema you deliberately excluded — it should fail
- For GitHub: try to push to a branch (if you scoped to read-only) — it should fail

**Deliverable:** A working `.mcp.json` with at least two servers, with documented permission scoping decisions.

---

## Exercise 3 — Deep (90 min): TCO Analysis for One Workflow

**Goal:** Build the business case for your workflow transformation.

Choose the workflow you mapped in Module 03 Exercise 3.

**Part 1 — Baseline measurement (20 min)**

For the past month, estimate:
- How many times did you do this workflow?
- Average time per instance?
- Total hours spent on this workflow last month?

**Part 2 — AI-native estimate (20 min)**

For the AI-native version:
- Time to run the agent + review output per instance?
- Time to set up the agent (one-time cost)?
- Time to write/maintain the data contract and quality gates?

**Part 3 — TCO calculation (15 min)**

```
Monthly time saved: [baseline hours] - [AI-native hours] = ___
Annual time saved: ___ × 12 = ___
Setup investment: [one-time hours] = ___
Break-even: [setup hours] / [monthly hours saved] = ___ months
```

**Part 4 — API cost estimate (15 min)**

Estimate your Claude API usage for this workflow:
- Average tokens per run (input: system + context + task; output: tool calls + final)
- Runs per month
- Cost per 1M tokens (check current Anthropic pricing)
- Monthly API cost

Is the API cost less than 10% of the time saved? (It almost certainly is, but verify.)

**Part 5 — Write the one-pager (20 min)**

```markdown
# Business Case: [Workflow Name] Automation

## Current State
- Time spent: [X hrs/month]
- Main pain points: [2-3 bullets]

## Proposed Change
[2-3 sentence description of the AI-native workflow]

## Quality Controls
[Quality gates, review checklist, rollback plan — 3-4 bullets]

## Investment Required
- Setup: [X hrs one-time]
- Ongoing: [X hrs/month for review and governance]

## Return
- Time saved: [X hrs/month]
- Break-even: [X months]
- Annual net benefit: [X hrs]

## Next Steps
1. [First concrete action]
2. [Second action]
3. [Third action]
```

This one-pager is deployable. Send it to your manager or tech lead.
