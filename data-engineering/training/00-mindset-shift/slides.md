---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
style: |
  h1 { color: #1a1a2e; }
  h2 { color: #16213e; }
  strong { color: #0066cc; }
  blockquote { border-left: 4px solid #0066cc; padding-left: 16px; color: #444; }
  .pain { background: #fff3cd; padding: 12px; border-radius: 6px; }
  .win  { background: #d4edda; padding: 12px; border-radius: 6px; }
---

# Let's Talk About Your Week

*Not a lecture. A conversation.*

*Module 00 · AI-Native Data Engineering*

---

# Quick show of hands

> "How many of you have written **essentially the same ETL script** more than five times in your career?"

&nbsp;

> "How many have had an analyst ping you for a SQL query while you were in the middle of something actually hard?"

&nbsp;

> "How many have written documentation for a pipeline — **after** it was already in production?"

---

# That's not a skills gap.

That's just the job as it exists today.

You are skilled. You know what you're doing.

And yet a big portion of your week is work that **doesn't require what makes you valuable.**

&nbsp;

What if it didn't have to be?

---

# Here's what happened at one team last quarter

> A data engineer got a request at 9am:
> *"New Stripe data source, needs to land in the warehouse by EOD, reconciled, documented."*
>
> **Old timeline**: 6–8 hours of writing, testing, debugging, documenting.
>
> **What actually happened**: She wrote the data contract in 30 minutes, described the schema and quality rules, and orchestrated an agent to build the pipeline. She reviewed and merged at 11am. By 2pm she was working on the actual hard problem — the architecture decision no one else could make.

This is not science fiction. This is happening now.

---

# "But will AI take my job?"

Let's address this directly.

SQL can be generated. Boilerplate can be generated. Documentation can be generated.

**What cannot be generated:**

- Knowing that "active customer" means different things to Finance and Marketing in *your company*
- Deciding that the new data source should be treated as PII
- Owning the relationship with the stakeholder who's been burned by bad data before
- Making the call to delay a release because the quality numbers don't look right

These are judgment calls. They are **irreplaceable**. And right now, they're buried under work that shouldn't require your level of skill.

---

# The actual risk

The risk is not that AI replaces data engineers.

> The risk is that data engineers who use AI
> **replace data engineers who don't.**

You're not here to be replaced. You're here to **get ahead of it.**

---

# What's actually changing

**Before**: You are the one who writes the pipeline.

**Now**: You are the one who **decides what the pipeline must do** — and you have a very fast executor at your disposal.

&nbsp;

The shift isn't in your value. It's in where you **apply** your value.

Less time writing code that follows known patterns.

More time on the decisions, architecture, and quality standards that actually require you.

---

# A day in the life — today vs 6 months from now

| Today | 6 Months From Now |
|-------|------------------|
| Write ETL script (3 hrs) | Define data contract, review agent output (45 min) |
| Debug failed pipeline (2 hrs) | Quality gate caught it in staging — investigate root cause (30 min) |
| Write analyst SQL (1 hr) | Text-to-SQL agent handles self-serve; you review high-stakes queries |
| Write pipeline docs (skipped) | Docs auto-generated — you edit 3 lines |
| **Total execution work: 6+ hrs** | **Total execution work: ~1.5 hrs** |

What happens with the other 4.5 hours?

You do the work that actually moves your career.

---

# This is not "vibe coding"

Let's be clear about what this isn't.

"Vibe coding" = prompt → accept → ship → hope

**That fails in enterprise** because it has no:
- Audit trail for compliance
- Quality gates for data trust
- Reproducibility for production stability
- Governance for stakeholder confidence

**What we're building is different.**

You design the standards. The agent executes against them. You review before anything ships.

Speed without rigor is just faster mistakes.

---

# The new role in one sentence

> You are the architect and quality owner.
> The agent is your fastest developer.

The agent doesn't decide what "correct" means. You do.

The agent doesn't decide what quality is acceptable. You do.

The agent doesn't decide whether the data is ready to trust. You do.

**Your judgment is the one thing in this stack that cannot be automated.**

---

# What we'll cover in this training

| Module | What You'll Get |
|--------|----------------|
| 01 | The landscape — what agents, skills, and MCP servers actually are |
| 02 | The methodology — how to plan, architect, and delegate properly (BMAD) |
| 03 | Your workflow — mapping what you do today to the AI-native version |
| 04 | The stack — which tools work best, and why |
| 05 | Enterprise patterns — governance, audit, compliance, production |

&nbsp;

By the end, you'll have a concrete map from where you are today to how you work in 6 months.

---

# Before we go on

Take 5 minutes. Write answers to these:

1. What's the most repetitive thing you do that makes you think "there has to be a better way"?
2. What's the work you *wish* you had more time for?
3. What's the one decision in your team that only you can make because of what you know?

Keep these. We'll come back to them in Module 04.

---

# One more thing

The goal of this training is not to turn you into an AI expert.

It is to make sure that six months from now, you are **more valuable** to your organization — not less — because you know how to use these tools with the rigor they require.

You're already good at this job.

Let's make sure you're great at the next version of it.
