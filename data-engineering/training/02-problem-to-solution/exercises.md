# Module 02: Exercises — From Problem to Acceptance Criteria

## Exercise 1: Decompose a Vague Request

**Scenario:** Your product owner sends you this message:

> "Can you build something that shows us how each customer segment is performing? I need it for the weekly exec review."

**Task:** Before writing any code, write the following:

1. **Three clarifying questions** you would ask the product owner before starting
2. **Two possible interpretations** of "customer segment performance" that would lead to completely different pipelines
3. **One functional requirement** that captures what you believe they actually want
4. **One non-functional requirement** they haven't mentioned but almost certainly need

---

## Exercise 2: Write Requirements for a Real Pipeline

**Task:** Pick a pipeline or report you currently own (or have recently built).

Write:
1. **Problem statement** (1–2 sentences): What business decision does this data support?
2. **Functional requirements** (bullet list): What does the pipeline produce? Be specific — column names, transformation rules, filter conditions, handling of edge cases.
3. **Non-functional requirements** (bullet list): Performance SLA, idempotency requirement, any PII/compliance constraints, observability requirement.
4. **Acceptance criteria** (numbered list, 4–6 items): How will you and the product owner verify this is done and correct?

**Reflection:** After writing these, ask yourself:
- Could you hand this to a colleague (or an AI agent) and be confident they'd build the same thing you would?
- Are there any acceptance criteria you couldn't actually test? If so, rewrite them until they're testable.

---

## Exercise 3: The Iteration Checkpoint

**Scenario:** You are two days into building a new pipeline. You have sample output for one day of data.

**Task:** Write the email or Slack message you would send to the product owner at this checkpoint.

Requirements for the message:
- Under 150 words
- Clearly states this is a prototype / work in progress
- Shows 3–5 rows of sample output (you can make them up)
- Asks one specific question about whether the output matches expectations
- Does NOT ask the product owner to "review everything" — ask one targeted question

**Why this matters:** The discipline of asking one specific question instead of "does this look right?" forces you to identify the highest-risk assumption in your current build.

---

## Exercise 4: Map Requirements to BMAD Phases

**Task:** For each of the following items, identify which BMAD phase it belongs to and what the output of that phase would be.

| Item | BMAD phase | Output |
|------|-----------|--------|
| "Revenue is gross minus refunds, not gross alone" | | |
| "Pipeline must complete in 20 min" | | |
| "Each agent task touches one table only" | | |
| "NULL product_id → category = unassigned" | | |
| "Prototype reviewed with product owner on Day 3" | | |
| "Quality gate: zero NULL customer_id rows" | | |

*(Answers: ANALYZE, ARCHITECT, DECOMPOSE, ANALYZE, IMPLEMENT, ARCHITECT)*

---

## Exercise 5: The Trust Conversation

**Task (stretch exercise):** Schedule a 30-minute meeting with the product owner for a pipeline you currently own.

In that meeting:
1. Show them the current output and ask: "Is this the number you use to make decisions?"
2. Ask: "What would have to be wrong for you to stop trusting this number?"
3. Ask: "If this pipeline stopped updating, how quickly would you notice and how would it affect you?"

After the meeting, write down:
- What you learned that isn't captured in any technical documentation
- One requirement you should add or change based on what you heard

**This is the most valuable 30 minutes you can spend on a data product you already own.**

---

## Reflection Prompts

After completing the exercises, consider:

1. How many of your current pipelines have written functional requirements? Written acceptance criteria?
2. Has a pipeline you built ever been questioned because the business logic was wrong — not the code, but the definition? What would have prevented that?
3. What is the earliest point in a build where you can show something to the product owner? What would that output look like?
