# Module 00: Learner's Reading Guide

*Read this after the session to reinforce what you experienced in the room.*

---

## The Honest Starting Point

If you're reading this, you're a working data engineer. You know your stack. You've shipped pipelines, debugged production failures at inconvenient hours, and answered a non-trivial number of Slack messages that started with "quick question about the data."

You did not come here because something was wrong with how you work.

You came here because the tools available to you are changing, and you'd rather be ahead of that change than behind it.

That's already the right instinct.

---

## What the Research Actually Shows

In 2026, 81% of organizations are tackling more complex data use cases with AI. The teams that are winning aren't the ones that replaced their data engineers — they're the ones whose data engineers learned to work differently.

One team reduced manual investigation time by 20–25 hours per week by adding three targeted agents to their quality and investigation workflow. The engineers didn't disappear. They moved their time to architecture decisions, stakeholder relationships, and data product strategy.

That's the pattern this training is built around.

---

## What Is Actually Changing

Think about the work you did last week. How much of it falls into these categories?

**Category A — Execution that follows known patterns:**
- Writing ETL logic for a new data source with a known schema
- Generating SQL for an analytical question
- Writing dbt tests for obvious quality rules
- Documenting a pipeline you just built
- Building a data quality check for nulls, duplicates, type issues

**Category B — Judgment that requires your context:**
- Deciding whether a new data source should be treated as PII
- Determining what "customer" means in this month's revenue report
- Deciding whether data quality is "good enough" to release
- Choosing the right grain for a data model
- Knowing which stakeholder to involve in a data discrepancy

Category A work is where AI agents are genuinely, substantially better than doing it manually. Category B work is irreplaceable — and that's where your career value lives.

The problem today: Category A takes up 60–80% of most data engineers' weeks, leaving little time for Category B.

The opportunity: Shift Category A to agents, so Category B is where you spend your time.

---

## The Quality Question

The most important thing to understand about AI-native data engineering is that it requires **more rigor, not less**.

When you write a pipeline yourself, your judgment is embedded in every line. When an agent writes a pipeline to your specification, your judgment has to be explicit upfront — in the data contract, the quality rules, the acceptance criteria. And it has to be verified on the way out — in the review process and quality gates.

This is actually better for the organization. The judgment is documented. The standards are written down. The quality thresholds are explicit. The pipeline can be reviewed by anyone on the team, not just the engineer who wrote it.

The discipline of defining your standards before execution is what separates AI-native data engineering from vibe coding. It's also what makes it enterprise-grade.

---

## The Fear Is Real, and Worth Addressing

"Will AI take data engineering jobs?"

Some roles will change significantly. The data engineer whose primary value is writing repetitive ETL scripts in slightly different configurations is most exposed. Not because they're not skilled — but because that specific skill is becoming significantly less scarce.

The data engineer who can:
- Define data contracts that make agent-generated code trustworthy
- Design multi-agent pipelines for complex data products
- Set quality standards that govern automated workflows
- Own the architecture decisions that determine what gets built
- Build the stakeholder relationships that translate business needs into data specifications

That engineer is substantially more valuable in an AI-native world, not less. Because AI makes the execution cheap — it makes the good judgment more expensive.

---

## Three Concepts to Hold Before Module 01

**1. Delegate execution, own judgment.**
Every task has an execution component and a judgment component. Agents handle execution. Your judgment is what makes agent output trustworthy.

**2. Quality gates are not optional.**
AI-generated output needs the same quality process as any other code — plus explicit data quality validation. The discipline doesn't decrease; the time to first draft decreases.

**3. Your reflection answers matter.**
The three questions from the session exercise:
- Most repetitive task (this goes to agents)
- Work you wish you had time for (this is where you'll spend the reclaimed time)
- Decision only you can make (this is your irreplaceable value)

Take these seriously. They are the foundation of your Module 03 workflow map.

---

## Before Module 01

Read: `references/tools-catalog.md` — get familiar with the tool landscape before the AI landscape session. You don't need to understand everything; just know what exists.

Bring to Module 01: one specific data source or pipeline from your current work. You'll use it as the example throughout the methodology modules.
