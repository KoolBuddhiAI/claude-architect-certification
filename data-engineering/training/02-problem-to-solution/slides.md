---
marp: true
theme: default
paginate: true
---

# The Missing Phase
## Why Engineers Build the Wrong Thing — Fast

**Module 02 — Claude Architect Certification: Data Engineering Track**

---

# The Pattern We All Recognise

> "The Jira ticket said 'daily revenue report.' I built it. Three weeks later: wrong definition of revenue, no GDPR filter, product owner never signed off, now it's in prod and nobody trusts it."

Sound familiar?

---

# The Real Problem

It's not a coding problem.

It's a **requirements problem**.

Engineers skip from **request** → **code**.

With AI, you now skip from **request** → **shipped code** in hours.

**Faster execution of the wrong thing is not progress. It is faster failure.**

---

# What Gets Skipped

| Step | What it catches |
|------|----------------|
| Problem definition | Are we solving the right thing? |
| Functional requirements | What should it actually do? |
| Non-functional requirements | How fast, how safe, how scalable? |
| Product owner alignment | Does this match their objective? |
| Acceptance criteria | How do we know we're done? |
| Iteration | Is this what they meant? |

Skip these → build the wrong thing at AI speed.

---

# The SDLC Was Annoying. It Was Also Right.

Old SDLC was slow because:
- Waterfall — requirements frozen upfront
- Long cycles before any feedback
- No room to adapt

What it got **right**:
- Force a conversation before writing code
- Define done before starting
- Show something before calling it finished

**BMAD keeps what was right and removes what was slow.**

---

# The Cost of Skipping Alignment

```
Without alignment:              With alignment:

Request received                Request received
      ↓                               ↓
Start coding                    30-min requirements session
      ↓                               ↓
Build for 2 weeks               Functional spec agreed
      ↓                               ↓
Demo to product owner           Build for 3 days
      ↓                               ↓
"That's not what I meant"       Demo (prototype)
      ↓                               ↓
Rebuild                         One round of feedback
      ↓                               ↓
Ship (3 weeks, wrong)           Ship (1 week, right)
```

---

# Functional vs Non-Functional Requirements

**Functional** — what the system does:
- "Produce a daily row per customer with revenue in USD"
- "Exclude test transactions (flag = 'test')"
- "Handle NULL product_id as category = 'unassigned'"

**Non-Functional** — how it does it:
- "Must complete within 30 minutes of midnight"
- "Must pass data quality checks before downstream tables refresh"
- "PII fields must not appear in logs"
- "Re-runs must be idempotent"

Both are required. Most engineers write neither.

---

# Acceptance Criteria: The Contract

Acceptance criteria answer: **"How will we know this is done and correct?"**

Bad: *"Build a revenue report"*

Good:
> - [ ] Revenue matches Stripe dashboard ± 0.1% for last 30 days
> - [ ] Zero rows with NULL customer_id
> - [ ] Runs in under 20 minutes on current data volume
> - [ ] Product owner has reviewed output on 3 days of data and signed off
> - [ ] dbt tests pass on every run

**If you can't write the acceptance criteria, you don't understand the requirement.**

---

# The Product Owner's Objective

Your product owner does not care about:
- Your pipeline architecture
- Whether you used dbt or Spark
- How elegant the SQL is

They care about:
- **Will the sales team trust this number?**
- **Can the CFO use it in the board deck?**
- **Does it update before the morning standup?**

Your job is to connect your technical work to their business outcome.

---

# Show Output. Iterate. Ship.

Don't build for three weeks and present at the end.

| Checkpoint | What to show |
|------------|-------------|
| Day 1 end | Sample output on 1 day of data — is the shape right? |
| Day 3 | Full output on 1 week — are the numbers plausible? |
| Day 5 | Full output on 30 days — review against acceptance criteria |
| Done | Sign-off on acceptance criteria → merge |

**Early feedback is cheap. Late feedback is expensive. AI makes this even more true.**

---

# Where BMAD Fits

BMAD phases map directly to the missing steps:

| Missing step | BMAD phase |
|---|---|
| Problem definition | ANALYZE — business question first |
| Functional requirements | ANALYZE — what does it produce? |
| Non-functional requirements | ARCHITECT — quality contract, SLAs |
| Product owner alignment | ANALYZE — stakeholder interviews |
| Acceptance criteria | ARCHITECT — quality gates = acceptance criteria |
| Show output and iterate | IMPLEMENT — prototype → review → refine |

BMAD is not a new bureaucracy. It is the minimal structure needed to build the right thing.

---

# The Discipline

> "But with AI, we can just try things and fix them."

Yes. And the product owner will stop trusting your output if it changes every week.

Enterprise data engineering requires:
- **Predictability** — stakeholders plan around your data
- **Auditability** — someone will ask why revenue changed
- **Trust** — the hardest thing to build, easiest to lose

Process protects trust. AI speed is only valuable when trust is intact.

---

# Before You Move On

- [ ] Write functional and non-functional requirements for a pipeline you own right now
- [ ] Write 3–5 acceptance criteria for that same pipeline
- [ ] Identify the product owner — have you ever aligned with them on what "done" means?
- [ ] In your next build, show output at Day 1 before continuing

**Next:** Module 03 — BMAD gives you the specific mechanics for each of these steps.

---

# Summary

1. Engineers skip requirements, design, and alignment
2. AI makes the consequence arrive faster
3. Functional + non-functional requirements define what to build
4. Acceptance criteria define when you're done
5. Iteration with the product owner catches misalignment early
6. BMAD is the lightweight process that enforces all of this
