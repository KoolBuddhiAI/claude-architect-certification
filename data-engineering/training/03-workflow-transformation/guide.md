# Module 03: Workflow Transformation — Reading Guide

## The Point of This Module

Every other module is conceptual. This one is personal.

The goal is to take each of the workflows you currently own and produce a specific "after" version — not as a general pattern, but for your actual stack, your actual tools, and your actual quality requirements.

Use your Module 00 reflection answers as you read through this. The most repetitive task you identified is your first candidate for transformation.

---

## ETL / ELT Pipelines

**The transformation:** You move from writing pipeline code to writing pipeline specifications.

In the old workflow, your judgment is embedded implicitly in every function call, every null check, every edge case handling. The risk: only you know why it works that way.

In the new workflow, your judgment is explicit in the data contract and quality gates. The agent implements against the spec. Any competent engineer (human or AI) can understand, review, and modify the pipeline because the reasoning is documented.

**The hard part:** Writing a good data contract takes practice. The first few you write will feel slow. By the fifth, it will feel natural. By the tenth, you'll wonder how you ever built pipelines without one.

**What to keep:** Your domain expertise is what makes the contract correct. The contract has to know that Stripe `amount_cents` is in cents, not dollars. It has to know that `customer_id` from your CRM doesn't match `customer_id` from your e-commerce platform. That knowledge is yours — not the agent's.

---

## Data Quality Management

**The transformation:** You move from reactive fire-fighting to proactive gate-keeping.

In the old workflow, data quality problems are discovered by consumers (analysts, stakeholders, dashboards that show wrong numbers). You investigate, find the root cause, fix it, and hope it doesn't happen again.

In the new workflow, quality issues are caught before data reaches consumers. The DQ agent runs against every pipeline output before it's promoted. Critical failures block promotion. Warnings trigger alerts. The quality report is a structured document, not an email thread.

**The shift in your role:** You no longer investigate individual data issues — you design the quality gates that prevent classes of issues. When a new issue escapes (and occasionally one will), your job is to update the quality contract to catch that class of issue in the future, not just fix the instance.

This is a more leveraged use of your time. One quality gate prevents dozens of future investigations.

---

## Power BI and Fabric Reporting

**The transformation:** You move from building reports to governing semantic models.

With Microsoft's `skills-for-fabric` bundle, Claude can:
- Create and modify semantic models
- Author PBIR report layouts
- Write DAX measures from natural language descriptions
- Publish to workspaces

**What this means for you:** Your job in reporting shifts from "build this report" to:
1. Define the semantic model correctly (which metrics, which dimensions, what does "revenue" mean in this context)
2. Review the model Claude generates for semantic correctness
3. Approve the DAX for accuracy on business-critical metrics
4. Govern the publication

The semantic correctness review is irreplaceable. Claude can write DAX that computes correctly given its understanding of the model — but your understanding of the business is what makes the metric definition right.

**Important:** Power BI Q&A (legacy NL feature) retires December 2026. The migration path is Claude + Fabric MCP. If your team uses Q&A, this is not optional.

---

## SQL for Analytics Requests

**The transformation:** You move from being the SQL writer to being the SQL architect and reviewer.

Text-to-SQL agents handle well-defined questions against well-documented schemas reliably. The validation-retry loop (`validate_sql` → fix → `execute_sql`) catches most errors before they reach you.

**Where you still review:**
- Any query touching financial data or metrics used in reporting
- Queries with complex business logic (rolling averages, cohort analysis, attribution)
- Queries that will be productionized (turned into a view, a dbt model, or a scheduled report)
- Anything an analyst says they'll "use for the board deck"

**Self-serve boundary:** Exploratory queries from analysts who understand the data → self-serve. Queries that will be shared, reported, or acted on → reviewed.

**The important design decision:** Where does the text-to-SQL agent live? Options:
- Claude Code for your team (DE-facing, well-governed)
- An internal API wrapping the agent (analyst-facing, easier to scope)
- A chat interface on top of your BI tool (broadest access, most governance complexity)

The right answer depends on your organization's data literacy and trust requirements.

---

## Schema Changes and Migrations

**The transformation:** You move from manually writing migration SQL to reviewing agent-generated migration plans.

The schema evolution agent (`data-engineering/04-schema-evolution-agent/`) does the work you used to do manually:
1. Diffs the schemas
2. Classifies each change as breaking or non-breaking
3. Generates forward SQL + rollback SQL
4. Produces a pre-deployment checklist

**Your review job:** Validate the classification. The agent's classification is usually correct, but you need to verify the "non-breaking" calls. A widening type change from `VARCHAR(15)` to `VARCHAR(20)` is technically non-breaking — but if a downstream system is reading that column with a fixed-width expectation, it breaks them. That context is yours.

**Never skip the rollback SQL review.** An untested rollback is not a rollback.

---

## Documentation and Data Catalog

**The transformation:** Documentation becomes a review task, not a writing task.

Agents can generate:
- Column descriptions from schema + data samples
- Pipeline documentation from lineage maps
- README files for data products
- dbt model descriptions

Your job: verify accuracy and add context that the agent can't infer. The agent can describe what a column contains. You add why it exists, what it replaced, and what quirks to know about.

A data engineer who generates and edits documentation produces 5x more documentation than one who writes it from scratch. Coverage improves. Freshness improves. The time cost drops to almost nothing.

---

## Your Personal Transformation Map

By the end of this module, you should have a document with this structure:

```
## [Your Name]'s Workflow Transformation Map

### Most Repetitive Task: [from Module 00]
Current workflow:
AI-native workflow:
What I still own:
Quality gate needed:

### Task I Wish I Had Time For: [from Module 00]
What's blocking it now:
How the transformation creates time for it:

### Decision Only I Can Make: [from Module 00]
Why it requires my context:
How the AI-native workflow gives me more time to make it well:
```

This document is your personal commitment. It's also the most concrete output from this entire training.

---

## Before You Move On

- [ ] For your most repetitive task, can you describe the AI-native version in a paragraph?
- [ ] What quality gate would make the agent-generated output trustworthy?
- [ ] Where is the boundary between self-serve SQL and reviewed SQL in your team?
- [ ] Do you use Power BI Q&A? If yes, have you looked at the Fabric Skills bundle?
- [ ] What does the schema evolution agent give you that you currently do manually?
