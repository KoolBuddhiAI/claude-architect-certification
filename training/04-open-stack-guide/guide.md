# Module 04: Open Stack Guide — Reading Guide

## The Question That Actually Matters

The wrong question: "Which tool does Claude work best with?"

The right question: "For each tool in my stack, what's the path to making it agent-accessible?"

Almost every modern data tool can be connected to Claude via an MCP server, a REST API integration, or a CLI Claude Code can invoke. The question isn't whether your stack works — it's how much friction is in the path.

---

## How to Evaluate Any Tool for AI-Native Compatibility

Five questions:

1. **Is there an MCP server?** The fastest path. If yes, you're connecting in 30 minutes.
2. **Is there a well-maintained Python/SDK client?** If yes, you can wrap it in a Claude tool function.
3. **Does it have structured output / schema?** Agents work best with structured data. A tool that returns unstructured text is harder to reason about.
4. **Does it have a CLI?** Claude Code can call CLIs via Bash tools. Not ideal but functional.
5. **Can Claude generate config/code for it?** If Claude has enough training data on the tool, it can scaffold configurations without hallucinating.

A tool that scores 5/5 has very low AI-native TCO. A tool that scores 1/5 requires significant custom work.

---

## The Warehouse Decision

Your warehouse is the most important tool choice because every data engineering workflow flows through it.

**For Microsoft Fabric / Power BI teams:**
The `skills-for-fabric` bundle is the clearest path. It's official, well-maintained, and covers the full Fabric surface area (warehouse, lakehouse, semantic models, reports). Claude Code with this skill bundle installed gives you near-native access to Fabric operations.

**For Google Cloud / BigQuery teams:**
Google ADK is purpose-built for this stack. The data science agent sample (see `references/adk-patterns.md`) shows the full pattern: root agent orchestrating database agent + data science agent + BQML sub-agent. The `before_agent_call` callback pattern for schema pre-loading is particularly worth adopting.

**For Snowflake teams:**
`mcp-snowflake` is actively maintained and covers the standard DML operations. Combine with dbt + dbt Cloud's API for the transformation layer.

**For PostgreSQL / open-source teams:**
`@modelcontextprotocol/server-postgres` is the reference MCP implementation. It's the most battle-tested and best-documented. Ideal for local development and self-hosted production.

**Cloud-agnostic principle:** Build your agent logic against the tool interface (MCP or SDK), not against the specific database syntax. When you need to swap databases, you swap the MCP connection — not the agent code.

---

## The Transformation Layer: Why dbt Is the Clear Leader

dbt has become the de facto standard for a reason that's even more relevant in an AI-native context: it separates the "what" (the transformation logic in `.sql` files) from the "how" (execution, testing, documentation).

Claude can generate dbt models from data contracts. Claude can generate dbt tests from quality gates. Claude can generate dbt documentation from lineage maps. And because dbt models are SQL files with a consistent structure, the generated code is easy to review.

The review question for agent-generated dbt models:
1. Does the SQL implement the transformation correctly? (Logic review)
2. Do the `schema.yml` tests cover the critical quality gates? (Quality review)
3. Is the model configured with the right materialization? (Performance review)

If your team doesn't use dbt yet, this is a strong reason to start.

---

## The Orchestration Decision

**Dagster vs Airflow:**

Dagster's asset-based model aligns naturally with the BMAD approach. A Dagster asset is the code representation of a data contract: it knows what it produces, what it depends on, and what quality checks apply to it. Claude generates Dagster assets from data contracts with high fidelity.

Airflow's DAG model works well too, but the lineage story is less direct. Claude generates Airflow DAGs from pipeline descriptions, but the connection between the DAG and the data contract is looser.

If you're starting a new project: Dagster. If you're on Airflow: add data contract documentation and Claude handles the rest.

**GitHub Actions for CI/CD:**
This is not optional for AI-native data engineering. Every agent-generated pipeline change goes through a PR. That PR runs automated tests. The quality gate agent runs in CI before any merge. GitHub Actions handles this cleanly, and Claude Code's headless mode integrates directly.

---

## TCO: The Full Calculation

When evaluating a tool in an AI-native context, add these factors to your standard TCO calculation:

**Costs that decrease with AI:**
- Engineer time on first-draft code generation (often 60–80% reduction)
- Documentation time (agent-generated + human review vs human-written)
- SQL request backlog for analysts (self-serve handles exploration tier)
- Time-to-first-prototype for new data products

**Costs that don't decrease:**
- Architecture decisions and data contract design
- Quality review time (same discipline, less writing)
- Stakeholder communication
- Production incident response (though quality gates reduce incidents)

**New costs:**
- API usage for Claude (model per query + context window)
- MCP server infrastructure (minimal if using hosted MCPs)
- Learning investment (one-time, estimated 40–80 hours for this full curriculum)

**The break-even point** for most data engineers: 2–6 weeks, depending on how repetitive their current work is.

---

## Before You Move On

- [ ] For your primary warehouse, which MCP server would you use?
- [ ] What's your team's transformation layer? Is there an MCP or Claude integration for it?
- [ ] Do you use dbt? If not, what's your current SQL transformation approach?
- [ ] What would the 5-question tool evaluation score be for your orchestration tool?
- [ ] Have you estimated the TCO impact for your most time-consuming workflow?
