# Module 06: The Missing Phase — Reading Guide

## The Problem No One Talks About

There is a failure mode that causes more wasted work in data engineering than bad code, bad infrastructure, or bad tooling combined: **building the right thing wrong** is bad, but **building the wrong thing right** is worse.

Engineers are trained to solve technical problems. Given a constraint, they optimize. Given a spec, they implement. What they are rarely trained to do is slow down before the spec exists and ask whether the spec describes the right problem.

AI accelerates execution. An engineer who previously took two weeks to build a pipeline can now do it in two days. What does not change is whether the pipeline was needed, whether it produces the right numbers, and whether the person who asked for it will actually trust it.

The missing phase is everything that happens *before* you open your editor.

---

## What the Product Owner Actually Wants

Product owners, data analysts, and business stakeholders are not asking for pipelines. They are asking for **decisions they can make with confidence**.

A CFO who asks for a "daily revenue report" wants to be able to walk into a board meeting, show a number, and defend it. They need:
- The number to be correct (obvious, often not achieved)
- The number to be consistent with other numbers they report (harder than it sounds)
- The number to update reliably before the meeting (operational requirement)
- Someone to be accountable when it is wrong (governance requirement)

None of these requirements are technical. All of them constrain your technical design.

If you build a pipeline without understanding these constraints, you will build something that produces a number — and that number will be questioned the first time it differs from what someone expected, and it will lose trust permanently.

---

## Functional Requirements: What the System Does

A functional requirement describes a behaviour the system must exhibit. It is testable and specific.

**Bad functional requirement:** "Process Stripe transactions"

**Good functional requirement:** "Produce one row per `customer_id` per day containing: `gross_revenue_usd` (sum of `amount_cents / 100` for completed transactions in USD), `refund_amount_usd` (sum of `refund_cents / 100`), `net_revenue_usd` = gross minus refunds. Exclude rows where `transaction_status != 'completed'`. Handle `NULL product_id` by assigning `category = 'unassigned'`."

Notice the difference: the good version tells an agent (or a human) exactly what to build. The bad version requires inference — and inference at AI speed means inconsistency at AI scale.

**Writing good functional requirements is a skill. Practice it.**

---

## Non-Functional Requirements: How the System Behaves

Non-functional requirements describe constraints on the system's behaviour: performance, reliability, security, and compliance. Engineers skip these most often.

Common non-functional requirements in data engineering:

**Performance:**
- "Must complete within 30 minutes of midnight so downstream tables are ready for 06:00 reports"
- "Must handle 10× current data volume without schema changes"

**Reliability:**
- "Re-runs must be idempotent — running twice must not duplicate rows"
- "Must fail loudly (alert on-call) rather than silently producing bad data"

**Security and compliance:**
- "PII fields (name, email, phone) must not appear in query logs"
- "Data must not leave the EU region"
- "Retention: raw data deleted after 90 days"

**Observability:**
- "Row count and quality metrics must be written to the monitoring table on every run"

Non-functional requirements often feel like "engineering concerns" that the business doesn't care about. They are not. A pipeline that produces correct numbers at midnight instead of 5am fails the product owner just as completely as one that produces wrong numbers.

---

## Acceptance Criteria: The Contract

Acceptance criteria are the agreed standard against which you will evaluate whether the work is complete and correct. They are not the same as requirements — they are the *tests* against which requirements are verified.

Good acceptance criteria are:
- **Binary** — pass or fail, not "looks reasonable"
- **Independent of implementation** — they test the output, not the code
- **Agreed in advance** — the product owner signs off before you start building

Example acceptance criteria for the revenue pipeline:

> 1. When run against the last 30 days of Stripe data, `net_revenue_usd` matches the Stripe dashboard figure ± 0.1%
> 2. No rows have `NULL customer_id` in the output
> 3. The pipeline completes in under 20 minutes on current data volume
> 4. All dbt tests pass on every run
> 5. The product owner has reviewed the output on 3 separate days of data and confirmed the numbers match expectations
> 6. A re-run of the same date range produces identical output (idempotency test)

If you cannot write acceptance criteria before starting, stop. You do not yet understand the requirement well enough to build it.

---

## The Iteration Loop

Even with good requirements and acceptance criteria, the first output will not be the final output. Plan for it.

The discipline here is: **show something early, show it often, and frame it explicitly as incomplete**.

| Checkpoint | What to show | What to ask |
|------------|-------------|-------------|
| End of Day 1 | Sample output on 1 day of data | "Is this the shape you expected? Is the column naming right?" |
| End of Day 3 | Full output on 1 week | "Do the weekly totals look plausible? Any surprises?" |
| End of Day 5 | Full output on 30 days | "Check against your acceptance criteria — does it pass?" |

Each checkpoint catches misalignment before it compounds. A product owner who sees a wrong column name on Day 1 saves you three days of work. The same discovery on Day 10 costs you a complete rebuild.

**This is not extra work. It replaces the rebuild you would otherwise have done.**

---

## How This Connects to BMAD

The BMAD methodology you will learn in Module 02 is the structured implementation of everything in this module:

- The ANALYZE phase is where you capture problem definition, functional requirements, and product owner objectives
- The ARCHITECT phase is where you formalise non-functional requirements, data contracts, and quality gates (which are your acceptance criteria)
- The DECOMPOSE phase is where you break requirements into testable agent tasks
- The IMPLEMENT phase is where you iterate — build, show, get feedback, refine

BMAD does not add process for process's sake. Every phase exists because skipping it produces a specific, observed failure mode.

---

## The Enterprise Trust Argument

Some engineers resist structured requirements because it feels slow. In a startup moving fast, this resistance has some validity. In enterprise data engineering, it does not.

Enterprise environments have a characteristic that makes trust uniquely fragile: **many people make decisions based on the same data**. When the CFO uses a revenue number, the VP of Sales uses the same number, and the product team uses the same number, any inconsistency affects all of them simultaneously. A loss of trust in a number is not easily recovered — the next time that number changes, every stakeholder will question it.

Process protects trust. Requirements documentation protects against "that's not what I asked for." Acceptance criteria documentation protects against "we agreed this was done." Iteration protects against the expensive rebuild.

AI speed is only valuable when the output is trusted. Trust is only maintained when the process is disciplined.

---

## Before You Move On

- [ ] Pick a pipeline you own. Write its functional requirements as if explaining to an agent what to build.
- [ ] Write its non-functional requirements — at minimum: performance, idempotency, and any compliance constraints.
- [ ] Write 3–5 acceptance criteria. Could you test each one with a SQL query or a dbt test?
- [ ] Identify the product owner. Have you ever had a requirements conversation with them? If not, schedule 30 minutes.
- [ ] In your next build, share a Day 1 prototype before doing further work.

**Coming up in Module 02:** BMAD gives you the specific tools — prompts, commands, and templates — to run each of these steps efficiently with Claude Code.
