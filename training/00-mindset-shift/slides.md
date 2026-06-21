---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
style: |
  h1 { color: #1a1a2e; }
  h2 { color: #16213e; }
  strong { color: #e94560; }
  .highlight { background: #f0f4ff; padding: 12px; border-left: 4px solid #4361ee; }
---

# The AI-Native Data Engineer
## A Mindset Shift — Not a Tool Update

*Module 00 · CCA-F Training Series*

---

# Why This Module Exists

Most AI training for data engineers focuses on **tools**.

This module focuses on **thinking**.

> The engineer who learns a new tool gets incrementally faster.
> The engineer who changes how they think gets **10× more valuable**.

---

# The Old Mental Model

```
Requirement → Write SQL → Debug SQL → Deploy → Done
```

You were the **executor**.

Your value was measured in:
- Lines of code shipped
- Pipelines built
- Queries optimized

---

# The New Mental Model

```
Requirement → Architect → Orchestrate Agents → Review → Govern → Done
```

You are now the **architect and the reviewer**.

Your value is measured in:
- Systems designed
- Outcomes delivered
- Quality guaranteed

---

# What Changed (and What Didn't)

| Still Yours | Now Delegated |
|---|---|
| Business context understanding | Boilerplate SQL generation |
| Data model design | Repetitive transformation code |
| Quality governance decisions | First-pass pipeline scaffolding |
| Stakeholder communication | Documentation drafting |
| Architecture decisions | Unit test generation |
| **Judgment** | Execution |

**Judgment cannot be automated. Execution can.**

---

# The Vibe Coding Trap

**Vibe coding**: prompt → accept → ship → hope

Works for:
- Personal projects
- Prototypes
- One-time scripts

**Fails for enterprise because:**
- No audit trail
- No reproducibility
- No governance
- No regression safety
- No stakeholder confidence

---

# Enterprise AI Development ≠ Vibe Coding

Enterprise requires:

1. **Documented decisions** — why this schema, why this model
2. **Reproducible pipelines** — same input = same output, always
3. **Audit trails** — who changed what, when, why
4. **Governed access** — least-privilege, role-based
5. **Tested outputs** — data quality gates, not trust

AI **accelerates** these — it does not replace them.

---

# The BMAD Principle

> "Planning is the multiplier."

Before any agent writes a line of code:

1. **Analyze** the problem fully
2. **Design** the architecture
3. **Decompose** into agent tasks
4. **Review** every agent output
5. **Govern** the deployed system

**The agent is your best developer, not your replacement.**

---

# Your New Job Description

**Before AI**: Write ETL pipelines, maintain SQL, fix broken schedules

**After AI**: 

- Define **data contracts** agents must respect
- Design **agent orchestration** for pipeline stages
- Set **quality gates** that block bad data automatically
- Own **lineage documentation** the agents produce
- Make **architecture decisions** that shape what agents build
- **Review and approve** agent-generated code before production

---

# The Trust Hierarchy

```
Your Business Judgment     ← Never delegate this
       ↓
Your Architecture Decisions ← Never delegate this
       ↓
Your Quality Gates          ← Define these, agents enforce them
       ↓
Agent-Generated Code        ← Review before shipping
       ↓
Agent-Generated Tests       ← Verify they cover the right cases
       ↓
Agent-Generated Docs        ← Edit, don't write from scratch
```

---

# A Tale of Two Engineers

**Engineer A** (tool mindset):
> "I use Claude to write SQL faster."

**Engineer B** (architect mindset):
> "I define data contracts and quality rules, then orchestrate agents to build and validate the full pipeline. I review the architecture and gate on quality metrics."

**Engineer B** is not just faster. They are doing a **different job** — one that is harder to automate.

---

# The Three Questions

Before starting any data engineering task, ask:

1. **What decision needs to be made here that requires my business context?**
2. **What can an agent do autonomously that I should specify and review instead of write?**
3. **What quality gate must exist so I can trust the output?**

These questions reshape every task from "I will code this" to "I will architect this."

---

# Module 00 — Key Takeaways

- You are an **architect and orchestrator**, not an executor
- Enterprise AI requires **more discipline**, not less
- **Vibe coding fails** at enterprise scale — methodology is non-negotiable
- Your irreplaceable value is **judgment, context, and governance**
- Every task has three layers: **decide → delegate → verify**

**Next: Module 01 — The AI Landscape for Data Engineers**

---

# Reflection Exercise

Before moving to Module 01, write answers to:

1. In your current role, what are the 3 most time-consuming tasks?
2. Which of those require genuine business judgment?
3. Which are execution that could be delegated to an agent?
4. What quality gates would you need to trust agent-delegated work?

*Keep these answers — you'll use them in Module 03 (Workflow Transformation).*
